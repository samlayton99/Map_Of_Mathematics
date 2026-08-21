/* charts.js - dependency-free SVG charting for the phase5 dashboard.
 *
 * Loaded with a plain <script> tag from a file:// page.
 * No imports, no modules, no build step. Defines exactly one global: window.Charts.
 *
 * API (every call is Charts.<name>(el, opts) -> the created <svg>, or null if el is unusable):
 *   Charts.bar(el, {series, title, yLabel, yMax, yFormat, horizontal})
 *   Charts.stacked(el, {rows, parts, title, yFormat, legend})
 *   Charts.lines(el, {series, xTicks, title, xLabel, yLabel, yFormat, vline, xType})
 *   Charts.heat(el, {rows, cols, values, title, format, min, max, colorLow, colorHigh, nullText})
 *   Charts.grouped(el, {groups, series, title, yLabel, yFormat, yMax})
 *
 * Theme: colours are read from the CSS custom properties --ink, --dim, --line, --card
 * on the target element, with hard fallbacks that follow prefers-color-scheme.
 *
 * Defensive by contract: no chart function throws. On malformed input it renders a
 * "no data" or error placeholder instead of taking the page down.
 */
(function (global) {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var FONT = 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';

  /* Categorical slots (dataviz reference palette, fixed order, never cycled). */
  var PALETTE_LIGHT = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7', '#e34948'];
  var PALETTE_DARK = ['#3987e5', '#d95926', '#199e70', '#c98500', '#d55181', '#008300', '#9085e9', '#e66767'];

  var FALLBACK_LIGHT = { ink: '#16161a', dim: '#6b6a65', line: '#d9d8d3', card: '#ffffff' };
  var FALLBACK_DARK = { ink: '#f2f1ee', dim: '#a3a29c', line: '#3a3a37', card: '#1a1a19' };

  /* ------------------------------------------------------------------ */
  /* small utilities                                                     */
  /* ------------------------------------------------------------------ */

  function isNum(v) {
    return typeof v === 'number' && isFinite(v);
  }

  function num(v, dflt) {
    var n = typeof v === 'number' ? v : parseFloat(v);
    return isFinite(n) ? n : dflt;
  }

  function arr(v) {
    return Object.prototype.toString.call(v) === '[object Array]' ? v : [];
  }

  function str(v, dflt) {
    if (v === null || v === undefined) return dflt === undefined ? '' : dflt;
    if (typeof v === 'string') return v;
    try { return String(v); } catch (e) { return dflt === undefined ? '' : dflt; }
  }

  function clamp(v, lo, hi) {
    return v < lo ? lo : (v > hi ? hi : v);
  }

  function docOf(el) {
    return (el && el.ownerDocument) || (typeof document !== 'undefined' ? document : null);
  }

  function viewOf(el) {
    var d = docOf(el);
    return (d && d.defaultView) || (typeof window !== 'undefined' ? window : null);
  }

  function prefersDark(el) {
    try {
      var w = viewOf(el);
      return !!(w && w.matchMedia && w.matchMedia('(prefers-color-scheme: dark)').matches);
    } catch (e) { return false; }
  }

  /* Resolve --ink / --dim / --line / --card off the target element. */
  function theme(el) {
    var base = prefersDark(el) ? FALLBACK_DARK : FALLBACK_LIGHT;
    var t = { ink: base.ink, dim: base.dim, line: base.line, card: base.card, dark: prefersDark(el) };
    try {
      var w = viewOf(el);
      if (!w || !w.getComputedStyle || !el) return t;
      var cs = w.getComputedStyle(el);
      if (!cs) return t;
      var keys = ['ink', 'dim', 'line', 'card'];
      for (var i = 0; i < keys.length; i++) {
        var v = cs.getPropertyValue ? cs.getPropertyValue('--' + keys[i]) : '';
        v = str(v).trim();
        if (v) t[keys[i]] = v;
      }
      /* If --ink was not supplied, inherited text colour beats a blind guess. */
      if (!str(cs.getPropertyValue ? cs.getPropertyValue('--ink') : '').trim()) {
        var c = str(cs.color).trim();
        if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') t.ink = c;
      }
    } catch (e) { /* computed style unavailable - fallbacks stand */ }
    return t;
  }

  function palette(el) {
    return prefersDark(el) ? PALETTE_DARK : PALETTE_LIGHT;
  }

  function seriesColor(el, given, index) {
    var g = str(given).trim();
    if (g) return g;
    var p = palette(el);
    return p[index % p.length];
  }

  /* Trim trailing zeros from a fixed-point string. */
  function trimZeros(s) {
    if (s.indexOf('.') < 0) return s;
    s = s.replace(/0+$/, '');
    return s.replace(/\.$/, '');
  }

  /* Default compact numeric formatter. Callers pass their own for percents etc. */
  function defaultFormat(n) {
    if (!isNum(n)) return '—';
    if (n === 0) return '0';
    var a = Math.abs(n);
    var sign = n < 0 ? '-' : '';
    if (a >= 1e12) return sign + trimZeros((a / 1e12).toFixed(1)) + 'T';
    if (a >= 1e9) return sign + trimZeros((a / 1e9).toFixed(1)) + 'B';
    if (a >= 1e6) return sign + trimZeros((a / 1e6).toFixed(1)) + 'M';
    if (a >= 1e4) return sign + trimZeros((a / 1e3).toFixed(1)) + 'k';
    if (a >= 1000) return sign + trimZeros(a.toFixed(0));
    if (a >= 100) return sign + trimZeros(a.toFixed(1));
    if (a >= 10) return sign + trimZeros(a.toFixed(2));
    if (a >= 1) return sign + trimZeros(a.toFixed(2));
    if (a >= 0.01) return sign + trimZeros(a.toFixed(3));
    return sign + a.toExponential(1);
  }

  function pctFormat(n) {
    if (!isNum(n)) return '—';
    var p = n * 100;
    if (Math.abs(p) >= 10) return p.toFixed(0) + '%';
    if (Math.abs(p) >= 1) return trimZeros(p.toFixed(1)) + '%';
    return trimZeros(p.toFixed(2)) + '%';
  }

  function fmtFn(f, dflt) {
    if (typeof f === 'function') {
      return function (n) {
        try {
          var out = f(n);
          return out === null || out === undefined ? '' : String(out);
        } catch (e) { return (dflt || defaultFormat)(n); }
      };
    }
    return dflt || defaultFormat;
  }

  /* Character-width estimate. No text measurement is available before layout. */
  function estWidth(text, fs) {
    return str(text).length * fs * 0.56;
  }

  function truncate(text, fs, maxW) {
    text = str(text);
    if (maxW <= 0) return '';
    if (estWidth(text, fs) <= maxW) return text;
    var maxChars = Math.floor(maxW / (fs * 0.56)) - 1;
    if (maxChars < 1) return '…';
    return text.slice(0, maxChars) + '…';
  }

  /* ------------------------------------------------------------------ */
  /* colour helpers                                                      */
  /* ------------------------------------------------------------------ */

  function parseColor(c) {
    c = str(c).trim();
    var m;
    if (/^#[0-9a-f]{3}$/i.test(c)) {
      return [parseInt(c[1] + c[1], 16), parseInt(c[2] + c[2], 16), parseInt(c[3] + c[3], 16)];
    }
    if (/^#[0-9a-f]{6}$/i.test(c)) {
      return [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)];
    }
    m = c.match(/^rgba?\(([^)]+)\)$/i);
    if (m) {
      var parts = m[1].split(/[\s,\/]+/).filter(function (s) { return s !== ''; });
      if (parts.length >= 3) {
        return [clamp(parseFloat(parts[0]) || 0, 0, 255), clamp(parseFloat(parts[1]) || 0, 0, 255), clamp(parseFloat(parts[2]) || 0, 0, 255)];
      }
    }
    return null;
  }

  function toHex(rgb) {
    function h(v) {
      var s = Math.round(clamp(v, 0, 255)).toString(16);
      return s.length < 2 ? '0' + s : s;
    }
    return '#' + h(rgb[0]) + h(rgb[1]) + h(rgb[2]);
  }

  function mixColor(a, b, t) {
    var ca = parseColor(a), cb = parseColor(b);
    if (!ca || !cb) return cb ? toHex(cb) : str(b, '#888888');
    t = clamp(num(t, 0), 0, 1);
    return toHex([
      ca[0] + (cb[0] - ca[0]) * t,
      ca[1] + (cb[1] - ca[1]) * t,
      ca[2] + (cb[2] - ca[2]) * t
    ]);
  }

  /* Relative luminance (WCAG). Used to pick readable text over a fill. */
  function luminance(c) {
    var rgb = parseColor(c);
    if (!rgb) return 1;
    function lin(v) {
      v = v / 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    }
    return 0.2126 * lin(rgb[0]) + 0.7152 * lin(rgb[1]) + 0.0722 * lin(rgb[2]);
  }

  function readableOn(fill) {
    return luminance(fill) > 0.42 ? '#101010' : '#ffffff';
  }

  /* ------------------------------------------------------------------ */
  /* svg construction                                                    */
  /* ------------------------------------------------------------------ */

  function make(doc, name, attrs) {
    var node = doc.createElementNS(NS, name);
    if (attrs) {
      for (var k in attrs) {
        if (!Object.prototype.hasOwnProperty.call(attrs, k)) continue;
        var v = attrs[k];
        if (v === null || v === undefined) continue;
        node.setAttribute(k, typeof v === 'number' ? round(v) : String(v));
      }
    }
    return node;
  }

  function round(n) {
    if (!isFinite(n)) return 0;
    return Math.round(n * 100) / 100;
  }

  function add(parent, node) {
    if (parent && node) parent.appendChild(node);
    return node;
  }

  function tip(doc, node, text) {
    if (!node || !text) return node;
    var t = doc.createElementNS(NS, 'title');
    t.textContent = str(text);
    node.appendChild(t);
    return node;
  }

  /* text() truncates to maxW and attaches the full string as a native tooltip. */
  function text(doc, parent, content, x, y, opts) {
    opts = opts || {};
    var fs = num(opts.size, 11);
    var full = str(content);
    var shown = opts.maxW ? truncate(full, fs, opts.maxW) : full;
    var node = make(doc, 'text', {
      x: x,
      y: y,
      fill: opts.fill || '#000',
      'font-size': fs,
      'font-weight': opts.weight || null,
      'text-anchor': opts.anchor || 'start',
      'dominant-baseline': opts.baseline || null,
      transform: opts.transform || null,
      opacity: opts.opacity === undefined ? null : opts.opacity,
      'pointer-events': 'none'
    });
    node.textContent = shown;
    if (shown !== full || opts.tip) tip(doc, node, opts.tip || full);
    return add(parent, node);
  }

  function clearEl(el) {
    if (!el) return;
    try {
      while (el.firstChild) el.removeChild(el.firstChild);
    } catch (e) {
      try { el.innerHTML = ''; } catch (e2) { /* give up quietly */ }
    }
  }

  function makeSvg(el, w, h, label) {
    var doc = docOf(el);
    var svg = make(doc, 'svg', {
      viewBox: '0 0 ' + round(w) + ' ' + round(h),
      width: '100%',
      preserveAspectRatio: 'xMidYMid meet',
      role: 'img',
      'font-family': FONT,
      'aria-label': label ? str(label) : null
    });
    try {
      svg.style.width = '100%';
      svg.style.height = 'auto';
      svg.style.maxWidth = '100%';
      svg.style.display = 'block';
    } catch (e) { /* style may be absent in exotic hosts */ }
    add(el, svg);
    return svg;
  }

  /* Bar geometry with the data-end rounded and the baseline end square. */
  function barPath(x, y, w, h, r, side) {
    x = round(x); y = round(y); w = round(w); h = round(h);
    r = Math.max(0, Math.min(num(r, 3), w / 2, h / 2));
    if (r <= 0.4) return 'M' + x + ',' + y + ' L' + (x + w) + ',' + y + ' L' + (x + w) + ',' + (y + h) + ' L' + x + ',' + (y + h) + ' Z';
    var x2 = x + w, y2 = y + h;
    switch (side) {
      case 'bottom':
        return 'M' + x + ',' + y + ' L' + x + ',' + (y2 - r) + ' Q' + x + ',' + y2 + ' ' + (x + r) + ',' + y2 +
          ' L' + (x2 - r) + ',' + y2 + ' Q' + x2 + ',' + y2 + ' ' + x2 + ',' + (y2 - r) + ' L' + x2 + ',' + y + ' Z';
      case 'right':
        return 'M' + x + ',' + y + ' L' + (x2 - r) + ',' + y + ' Q' + x2 + ',' + y + ' ' + x2 + ',' + (y + r) +
          ' L' + x2 + ',' + (y2 - r) + ' Q' + x2 + ',' + y2 + ' ' + (x2 - r) + ',' + y2 + ' L' + x + ',' + y2 + ' Z';
      case 'left':
        return 'M' + x2 + ',' + y + ' L' + (x + r) + ',' + y + ' Q' + x + ',' + y + ' ' + x + ',' + (y + r) +
          ' L' + x + ',' + (y2 - r) + ' Q' + x + ',' + y2 + ' ' + (x + r) + ',' + y2 + ' L' + x2 + ',' + y2 + ' Z';
      default: /* 'top' */
        return 'M' + x + ',' + y2 + ' L' + x + ',' + (y + r) + ' Q' + x + ',' + y + ' ' + (x + r) + ',' + y +
          ' L' + (x2 - r) + ',' + y + ' Q' + x2 + ',' + y + ' ' + x2 + ',' + (y + r) + ' L' + x2 + ',' + y2 + ' Z';
    }
  }

  /* ------------------------------------------------------------------ */
  /* ticks                                                               */
  /* ------------------------------------------------------------------ */

  function log10(v) { return Math.log(v) / Math.LN10; }

  function niceTicks(lo, hi, count) {
    if (!isNum(lo) || !isNum(hi)) return [0];
    count = Math.max(2, Math.round(num(count, 5)));
    if (lo > hi) { var t = lo; lo = hi; hi = t; }
    if (lo === hi) {
      if (lo === 0) return [0, 1];
      lo = Math.min(0, lo); hi = Math.max(0, hi);
      if (lo === hi) hi = lo + 1;
    }
    var span = hi - lo;
    var step = Math.pow(10, Math.floor(log10(span / count)));
    var err = span / count / step;
    if (err >= 7.5) step *= 10;
    else if (err >= 3.5) step *= 5;
    else if (err >= 1.5) step *= 2;
    var out = [];
    var start = Math.ceil(lo / step - 1e-9) * step;
    for (var v = start, guard = 0; v <= hi + step * 1e-6 && guard < 200; v += step, guard++) {
      var val = Math.abs(v) < step * 1e-9 ? 0 : Math.round(v / step) * step;
      out.push(parseFloat(val.toPrecision(12)));
    }
    return out.length ? out : [lo, hi];
  }

  function logTicks(lo, hi) {
    var out = [];
    if (!(lo > 0) || !(hi > 0)) return out;
    /* Decade span from the real range: deriving it from the padded integer
       bounds below overstates it (log10(0.01) is -2.0000000000000004). */
    var span = log10(hi) - log10(lo);
    var mantissas = span <= 1.05 ? [1, 2, 3, 4, 5, 6, 7, 8, 9]
      : (span <= 3.05 ? [1, 2, 5] : [1]);
    var d0 = Math.floor(log10(lo) - 1e-9);
    var d1 = Math.ceil(log10(hi) + 1e-9);
    for (var d = d0; d <= d1 && out.length < 60; d++) {
      for (var i = 0; i < mantissas.length; i++) {
        var v = mantissas[i] * Math.pow(10, d);
        if (v >= lo * (1 - 1e-9) && v <= hi * (1 + 1e-9)) out.push(parseFloat(v.toPrecision(12)));
      }
    }
    /* Thin out an over-dense axis rather than overprinting labels. */
    while (out.length > 12) {
      var thinned = [];
      for (var k = 0; k < out.length; k += 2) thinned.push(out[k]);
      if (thinned[thinned.length - 1] !== out[out.length - 1]) thinned.push(out[out.length - 1]);
      out = thinned;
    }
    if (!out.length) out = [lo, hi];
    return out;
  }

  /* ------------------------------------------------------------------ */
  /* shared chrome: title, legend, empty states                          */
  /* ------------------------------------------------------------------ */

  var TITLE_H = 24;

  function drawTitle(doc, svg, title, w, th) {
    if (!title) return;
    text(doc, svg, title, 4, 15, { size: 13, weight: '600', fill: th.ink, maxW: w - 8 });
  }

  /* Wrap legend swatches across the available width. Returns {height, draw(y)}. */
  function layoutLegend(doc, svg, items, w, th) {
    items = arr(items).filter(function (it) { return it && str(it.label) !== ''; });
    if (!items.length) return { height: 0, draw: function () {} };
    var fs = 11, sw = 9, gapIn = 5, gapOut = 14, lineH = 17;
    var lines = [[]], cur = 0, x = 0;
    for (var i = 0; i < items.length; i++) {
      var label = truncate(items[i].label, fs, Math.max(40, w * 0.45));
      var itemW = sw + gapIn + estWidth(label, fs);
      if (x > 0 && x + itemW > w - 4) { lines.push([]); cur++; x = 0; }
      lines[cur].push({ label: label, full: items[i].label, color: items[i].color, dashed: !!items[i].dashed, x: x, w: itemW });
      x += itemW + gapOut;
    }
    return {
      height: lines.length * lineH + 4,
      draw: function (top) {
        for (var li = 0; li < lines.length; li++) {
          var y = top + li * lineH + 9;
          for (var k = 0; k < lines[li].length; k++) {
            var it = lines[li][k];
            if (it.dashed) {
              add(svg, make(doc, 'line', {
                x1: it.x, y1: y, x2: it.x + sw, y2: y,
                stroke: it.color, 'stroke-width': 2.5, 'stroke-dasharray': '3 2', 'stroke-linecap': 'round'
              }));
            } else {
              add(svg, make(doc, 'rect', { x: it.x, y: y - 4.5, width: sw, height: 9, rx: 2.5, fill: it.color }));
            }
            text(doc, svg, it.label, it.x + sw + gapIn, y + 4, {
              size: fs, fill: th.dim, tip: it.label === it.full ? null : it.full
            });
          }
        }
      }
    };
  }

  function placeholder(el, title, message, state) {
    var doc = docOf(el);
    if (!doc) return null;
    var th = theme(el);
    var w = 480, h = title ? 132 : 108;
    var svg = makeSvg(el, w, h, title ? title + ' — ' + message : message);
    svg.setAttribute('data-state', state || 'empty');
    drawTitle(doc, svg, title, w, th);
    add(svg, make(doc, 'rect', {
      x: 1, y: title ? TITLE_H : 1, width: w - 2, height: h - (title ? TITLE_H : 0) - 2,
      rx: 6, fill: 'none', stroke: th.line, 'stroke-width': 1, 'stroke-dasharray': '4 4'
    }));
    text(doc, svg, message, w / 2, (h + (title ? TITLE_H : 0)) / 2 + 4, {
      size: 12, fill: th.dim, anchor: 'middle'
    });
    return svg;
  }

  function noData(el, title) {
    return placeholder(el, title, 'no data', 'empty');
  }

  /* Every public entry point runs through here: clear, render, never throw. */
  function guard(name, fn) {
    return function (el, opts) {
      /* Anything that is not a usable element is a silent no-op, not a fault. */
      if (!el || typeof el.appendChild !== 'function' || !docOf(el)) return null;
      try {
        clearEl(el);
        return fn(el, opts && typeof opts === 'object' ? opts : {});
      } catch (err) {
        try {
          if (global.console && console.error) console.error('[Charts.' + name + ']', err);
        } catch (e) { /* no console */ }
        try {
          clearEl(el);
          return placeholder(el, opts && opts.title, 'chart unavailable', 'error');
        } catch (e2) { return null; }
      }
    };
  }

  /* ------------------------------------------------------------------ */
  /* 1. bar                                                              */
  /* ------------------------------------------------------------------ */

  function drawBar(el, o) {
    var doc = docOf(el), th = theme(el);
    var title = str(o.title);
    var fmt = fmtFn(o.yFormat);

    var series = arr(o.series).filter(function (s) { return s && typeof s === 'object'; }).map(function (s, i) {
      var ci = arr(s.ci);
      var lo = isNum(ci[0]) ? ci[0] : (isNum(parseFloat(ci[0])) ? parseFloat(ci[0]) : null);
      var hi = isNum(ci[1]) ? ci[1] : (isNum(parseFloat(ci[1])) ? parseFloat(ci[1]) : null);
      if (lo !== null && hi !== null && lo > hi) { var t = lo; lo = hi; hi = t; }
      return {
        label: str(s.label, 'item ' + (i + 1)),
        value: isNum(s.value) ? s.value : num(s.value, null),
        lo: lo, hi: hi,
        /* One measure, one hue. Cycling hues per bar would encode nothing.
           A caller who wants a bar highlighted passes an explicit colour. */
        color: seriesColor(el, s.color, 0)
      };
    });

    var withData = series.filter(function (s) { return isNum(s.value); });
    if (!series.length || !withData.length) return noData(el, title);

    /* value domain, always anchored at zero */
    var dmin = 0, dmax = 0;
    for (var i = 0; i < withData.length; i++) {
      var s = withData[i];
      dmin = Math.min(dmin, s.value, isNum(s.lo) ? s.lo : Infinity);
      dmax = Math.max(dmax, s.value, isNum(s.hi) ? s.hi : -Infinity);
    }
    if (isNum(o.yMax)) dmax = Math.max(dmax, o.yMax);
    if (dmin === dmax) dmax = dmin + 1;

    return o.horizontal ? barHorizontal(el, doc, th, o, series, title, fmt, dmin, dmax)
      : barVertical(el, doc, th, o, series, title, fmt, dmin, dmax);
  }

  function barVertical(el, doc, th, o, series, title, fmt, dmin, dmax) {
    var n = series.length;
    var W = 760;
    var titleH = title ? TITLE_H : 0;
    var top = titleH + 16;
    var bottom = 36;
    var yLabel = str(o.yLabel);

    var ticks = niceTicks(dmin, dmax, 5);
    var tickFs = 10, maxTickW = 0;
    for (var i = 0; i < ticks.length; i++) maxTickW = Math.max(maxTickW, estWidth(fmt(ticks[i]), tickFs));
    var left = Math.min(120, Math.max(30, maxTickW + 10)) + (yLabel ? 16 : 0);
    var right = 14;

    var plotW = W - left - right;
    var plotH = 250;
    var H = top + plotH + bottom;
    var lo = Math.min(dmin, ticks[0]);
    var hi = Math.max(dmax, ticks[ticks.length - 1]);
    if (lo === hi) hi = lo + 1;

    var svg = makeSvg(el, W, H, title || 'bar chart');
    drawTitle(doc, svg, title, W, th);

    function y(v) { return top + plotH - ((v - lo) / (hi - lo)) * plotH; }

    /* gridlines + y ticks */
    for (var t = 0; t < ticks.length; t++) {
      var gy = y(ticks[t]);
      add(svg, make(doc, 'line', { x1: left, y1: gy, x2: left + plotW, y2: gy, stroke: th.line, 'stroke-width': 1 }));
      text(doc, svg, fmt(ticks[t]), left - 6, gy + 3.5, { size: tickFs, fill: th.dim, anchor: 'end' });
    }
    if (lo < 0) {
      add(svg, make(doc, 'line', { x1: left, y1: y(0), x2: left + plotW, y2: y(0), stroke: th.dim, 'stroke-width': 1.25 }));
    }
    if (yLabel) {
      text(doc, svg, yLabel, 0, 0, {
        size: 10.5, fill: th.dim, anchor: 'middle',
        transform: 'translate(' + round(11) + ',' + round(top + plotH / 2) + ') rotate(-90)',
        maxW: plotH
      });
    }

    var bandW = plotW / n;
    var barW = Math.min(52, Math.max(3, bandW * 0.62));

    for (var b = 0; b < n; b++) {
      var s = series[b];
      var cx = left + bandW * (b + 0.5);
      text(doc, svg, s.label, cx, top + plotH + 22, { size: 10.5, fill: th.dim, anchor: 'middle', maxW: bandW - 4 });
      if (!isNum(s.value)) continue;

      var y0 = y(0), yv = y(s.value);
      var barTop = Math.min(y0, yv), barH = Math.max(1, Math.abs(y0 - yv));
      var up = s.value >= 0;
      var rect = add(svg, make(doc, 'path', {
        d: barPath(cx - barW / 2, barTop, barW, barH, 4, up ? 'top' : 'bottom'),
        fill: s.color
      }));
      tip(doc, rect, s.label + ': ' + fmt(s.value) + (isNum(s.lo) && isNum(s.hi) ? '  [' + fmt(s.lo) + ', ' + fmt(s.hi) + ']' : ''));

      var labelY = up ? barTop - 6 : barTop + barH + 13;
      if (isNum(s.lo) && isNum(s.hi)) {
        var yl = y(s.lo), yh = y(s.hi);
        var capW = Math.min(9, barW * 0.45);
        var g = add(svg, make(doc, 'g', { stroke: th.ink, 'stroke-width': 1.25, opacity: 0.72, fill: 'none' }));
        add(g, make(doc, 'line', { x1: cx, y1: yh, x2: cx, y2: yl }));
        add(g, make(doc, 'line', { x1: cx - capW, y1: yh, x2: cx + capW, y2: yh }));
        add(g, make(doc, 'line', { x1: cx - capW, y1: yl, x2: cx + capW, y2: yl }));
        labelY = up ? Math.min(labelY, yh - 6) : Math.max(labelY, yl + 13);
      }
      labelY = clamp(labelY, top + 9, top + plotH + 11);
      text(doc, svg, fmt(s.value), cx, labelY, {
        size: 10.5, weight: '600', fill: th.ink, anchor: 'middle', maxW: bandW
      });
    }
    return svg;
  }

  function barHorizontal(el, doc, th, o, series, title, fmt, dmin, dmax) {
    var n = series.length;
    var W = 760;
    var titleH = title ? TITLE_H : 0;
    var labelFs = 11, valueFs = 10.5;

    var maxLabel = 0;
    for (var i = 0; i < n; i++) maxLabel = Math.max(maxLabel, estWidth(series[i].label, labelFs));
    var left = clamp(Math.ceil(maxLabel) + 10, 60, 250);

    var maxVal = 0;
    for (var v = 0; v < n; v++) {
      if (isNum(series[v].value)) maxVal = Math.max(maxVal, estWidth(fmt(series[v].value), valueFs));
    }
    var right = clamp(Math.ceil(maxVal) + 14, 34, 110);

    var rowH = 28, barH = Math.min(18, rowH * 0.6);
    var top = titleH + 8;
    var yLabel = str(o.yLabel);
    var bottom = 26 + (yLabel ? 14 : 0);
    var plotW = W - left - right;
    var plotH = n * rowH;
    var H = top + plotH + bottom;

    var ticks = niceTicks(dmin, dmax, 5);
    var lo = Math.min(dmin, ticks[0]);
    var hi = Math.max(dmax, ticks[ticks.length - 1]);
    if (lo === hi) hi = lo + 1;

    var svg = makeSvg(el, W, H, title || 'bar chart');
    drawTitle(doc, svg, title, W, th);

    function x(val) { return left + ((val - lo) / (hi - lo)) * plotW; }

    for (var t = 0; t < ticks.length; t++) {
      var gx = x(ticks[t]);
      add(svg, make(doc, 'line', { x1: gx, y1: top, x2: gx, y2: top + plotH, stroke: th.line, 'stroke-width': 1 }));
      text(doc, svg, fmt(ticks[t]), gx, top + plotH + 15, { size: 10, fill: th.dim, anchor: 'middle' });
    }
    if (lo < 0) {
      add(svg, make(doc, 'line', { x1: x(0), y1: top, x2: x(0), y2: top + plotH, stroke: th.dim, 'stroke-width': 1.25 }));
    }
    if (yLabel) {
      text(doc, svg, yLabel, left + plotW / 2, H - 4, { size: 10.5, fill: th.dim, anchor: 'middle', maxW: plotW });
    }

    for (var b = 0; b < n; b++) {
      var s = series[b];
      var cy = top + rowH * (b + 0.5);
      text(doc, svg, s.label, left - 8, cy + 3.5, {
        size: labelFs, fill: th.ink, anchor: 'end', maxW: left - 12, tip: s.label
      });
      if (!isNum(s.value)) {
        text(doc, svg, '—', x(0) + 6, cy + 3.5, { size: valueFs, fill: th.dim });
        continue;
      }
      var x0 = x(0), xv = x(s.value);
      var bx = Math.min(x0, xv), bw = Math.max(1, Math.abs(xv - x0));
      var pos = s.value >= 0;
      var rect = add(svg, make(doc, 'path', {
        d: barPath(bx, cy - barH / 2, bw, barH, 4, pos ? 'right' : 'left'),
        fill: s.color
      }));
      tip(doc, rect, s.label + ': ' + fmt(s.value) + (isNum(s.lo) && isNum(s.hi) ? '  [' + fmt(s.lo) + ', ' + fmt(s.hi) + ']' : ''));

      var endX = pos ? bx + bw : bx;
      if (isNum(s.lo) && isNum(s.hi)) {
        var xl = x(s.lo), xh = x(s.hi);
        var capH = Math.min(5, barH * 0.4);
        var g = add(svg, make(doc, 'g', { stroke: th.ink, 'stroke-width': 1.25, opacity: 0.72, fill: 'none' }));
        add(g, make(doc, 'line', { x1: xl, y1: cy, x2: xh, y2: cy }));
        add(g, make(doc, 'line', { x1: xl, y1: cy - capH, x2: xl, y2: cy + capH }));
        add(g, make(doc, 'line', { x1: xh, y1: cy - capH, x2: xh, y2: cy + capH }));
        endX = pos ? Math.max(endX, xh) : Math.min(endX, xl);
      }
      var vlabel = fmt(s.value);
      var vw = estWidth(vlabel, valueFs);
      var tx, anchor;
      if (pos) {
        tx = endX + 6; anchor = 'start';
      } else {
        tx = endX - 6; anchor = 'end';
        /* Would collide with the category-label gutter: move it clear of zero. */
        if (tx - vw < left + 2) { tx = x0 + 6; anchor = 'start'; }
      }
      if (anchor === 'start' && tx + vw > W - 2) { tx = W - 2; anchor = 'end'; }
      text(doc, svg, vlabel, tx, cy + 3.5, {
        size: valueFs, weight: '600', fill: th.ink, anchor: anchor
      });
    }
    return svg;
  }

  /* ------------------------------------------------------------------ */
  /* 2. stacked                                                          */
  /* ------------------------------------------------------------------ */

  function drawStacked(el, o) {
    var doc = docOf(el), th = theme(el);
    var title = str(o.title);
    /* values are documented as fractions summing to ~1, so percent is the useful default */
    var fmt = fmtFn(o.yFormat, pctFormat);

    var rows = arr(o.rows).filter(function (r) { return r && typeof r === 'object'; }).map(function (r, i) {
      return { label: str(r.label, 'row ' + (i + 1)), values: (r.values && typeof r.values === 'object') ? r.values : {} };
    });

    var parts = arr(o.parts).filter(function (p) { return p && typeof p === 'object'; }).map(function (p, i) {
      return { name: str(p.name, 'part ' + (i + 1)), color: seriesColor(el, p.color, i) };
    });

    /* If parts were omitted, derive them from the first row that has keys. */
    if (!parts.length) {
      var seen = {};
      for (var r = 0; r < rows.length; r++) {
        for (var k in rows[r].values) {
          if (Object.prototype.hasOwnProperty.call(rows[r].values, k) && !seen[k]) {
            seen[k] = 1;
            parts.push({ name: k, color: seriesColor(el, null, parts.length) });
          }
        }
      }
    }

    var anyValue = false;
    for (var i = 0; i < rows.length; i++) {
      for (var j = 0; j < parts.length; j++) {
        if (isNum(num(rows[i].values[parts[j].name], null))) { anyValue = true; break; }
      }
      if (anyValue) break;
    }
    if (!rows.length || !parts.length || !anyValue) return noData(el, title);

    var W = 760;
    var labelFs = 11;
    var maxLabel = 0;
    for (var m = 0; m < rows.length; m++) maxLabel = Math.max(maxLabel, estWidth(rows[m].label, labelFs));
    var left = clamp(Math.ceil(maxLabel) + 10, 60, 250);
    var right = 12;
    var plotW = W - left - right;

    var titleH = title ? TITLE_H : 0;
    var legend = o.legend === false ? { height: 0, draw: function () {} } : null;
    var rowH = 32, barH = 20;

    var svg = makeSvg(el, W, 10, title || 'stacked bar chart');
    if (!legend) {
      legend = layoutLegend(doc, svg, parts.map(function (p) { return { label: p.name, color: p.color }; }), W, th);
    }
    var top = titleH + legend.height + 4;
    var H = top + rows.length * rowH + 8;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + round(H));

    drawTitle(doc, svg, title, W, th);
    legend.draw(titleH + 2);

    for (var ri = 0; ri < rows.length; ri++) {
      var row = rows[ri];
      var cy = top + rowH * ri + rowH / 2;
      text(doc, svg, row.label, left - 8, cy + 3.5, {
        size: labelFs, fill: th.ink, anchor: 'end', maxW: left - 12, tip: row.label
      });

      var vals = [], sum = 0;
      for (var pi = 0; pi < parts.length; pi++) {
        var v = num(row.values[parts[pi].name], 0);
        if (!isNum(v) || v < 0) v = 0;
        vals.push(v);
        sum += v;
      }
      if (!(sum > 0)) {
        add(svg, make(doc, 'rect', {
          x: left, y: cy - barH / 2, width: plotW, height: barH, rx: 4,
          fill: 'none', stroke: th.line, 'stroke-width': 1, 'stroke-dasharray': '3 3'
        }));
        text(doc, svg, 'no data', left + plotW / 2, cy + 3.5, { size: 10, fill: th.dim, anchor: 'middle' });
        continue;
      }

      var cursor = left;
      for (var s = 0; s < parts.length; s++) {
        var frac = vals[s] / sum;
        if (!(frac > 0)) continue;
        var segW = frac * plotW;
        var drawW = Math.max(1, segW - (s < parts.length - 1 ? 2 : 0)); /* 2px surface gap */
        var seg = add(svg, make(doc, 'rect', {
          x: cursor, y: cy - barH / 2, width: drawW, height: barH,
          rx: Math.min(3, drawW / 2), fill: parts[s].color
        }));
        tip(doc, seg, row.label + ' — ' + parts[s].name + ': ' + fmt(frac));

        /* Under ~4% the text cannot be read: keep the segment, drop the label. */
        var lbl = fmt(frac);
        if (frac >= 0.04 && estWidth(lbl, 10) + 6 <= drawW) {
          text(doc, svg, lbl, cursor + drawW / 2, cy + 3.5, {
            size: 10, weight: '600', fill: readableOn(parts[s].color), anchor: 'middle'
          });
        }
        cursor += segW;
      }
    }
    return svg;
  }

  /* ------------------------------------------------------------------ */
  /* 3. lines                                                            */
  /* ------------------------------------------------------------------ */

  function drawLines(el, o) {
    var doc = docOf(el), th = theme(el);
    var title = str(o.title);
    var fmt = fmtFn(o.yFormat);
    var isLog = str(o.xType).toLowerCase() === 'log';

    var series = arr(o.series).filter(function (s) { return s && typeof s === 'object'; }).map(function (s, i) {
      var pts = arr(s.points).map(function (p) {
        if (!p || typeof p !== 'object') return null;
        var x = num(p.x, null), y = isNum(p.y) ? p.y : num(p.y, null);
        if (!isNum(x)) return null;
        if (isLog && !(x > 0)) return null; /* non-positive x cannot be placed on a log axis */
        return { x: x, y: isNum(y) ? y : null };
      }).filter(function (p) { return !!p; });
      pts.sort(function (a, b) { return a.x - b.x; });
      return {
        label: str(s.label, 'series ' + (i + 1)),
        color: seriesColor(el, s.color, i),
        dashed: !!s.dashed,
        points: pts
      };
    });

    var xs = [], ys = [];
    for (var i = 0; i < series.length; i++) {
      for (var j = 0; j < series[i].points.length; j++) {
        var p = series[i].points[j];
        if (isNum(p.y)) { xs.push(p.x); ys.push(p.y); }
      }
    }
    if (!series.length || !ys.length) return noData(el, title);

    var xlo = Math.min.apply(null, xs), xhi = Math.max.apply(null, xs);
    var ylo = Math.min.apply(null, ys), yhi = Math.max.apply(null, ys);

    if (isLog) {
      if (!(xlo > 0)) xlo = 1e-6;
      if (xlo === xhi) { xlo = xlo / 10; xhi = xhi * 10; }
    } else if (xlo === xhi) {
      var pad = Math.abs(xlo) > 0 ? Math.abs(xlo) * 0.1 : 1;
      xlo -= pad; xhi += pad;
    }

    var yTicks = niceTicks(ylo, yhi, 5);
    ylo = Math.min(ylo, yTicks[0]);
    yhi = Math.max(yhi, yTicks[yTicks.length - 1]);
    if (ylo === yhi) yhi = ylo + 1;

    var W = 760;
    var titleH = title ? TITLE_H : 0;
    var xLabel = str(o.xLabel), yLabel = str(o.yLabel);

    var tickFs = 10, maxTickW = 0;
    for (var t = 0; t < yTicks.length; t++) maxTickW = Math.max(maxTickW, estWidth(fmt(yTicks[t]), tickFs));
    var left = Math.min(120, Math.max(30, maxTickW + 10)) + (yLabel ? 16 : 0);
    var right = 16;
    var plotW = W - left - right;
    var plotH = 270;
    var bottom = 26 + (xLabel ? 15 : 0);

    var svg = makeSvg(el, W, 10, title || 'line chart');
    var legend = layoutLegend(doc, svg, series.map(function (s) {
      return { label: s.label, color: s.color, dashed: s.dashed };
    }), W, th);
    var top = titleH + legend.height + 10;
    var H = top + plotH + bottom;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + round(H));

    drawTitle(doc, svg, title, W, th);
    legend.draw(titleH + 2);

    function X(v) {
      if (isLog) {
        if (!(v > 0)) return left;
        var d = log10(xhi) - log10(xlo);
        return left + (d === 0 ? 0.5 : (log10(v) - log10(xlo)) / d) * plotW;
      }
      return left + ((v - xlo) / (xhi - xlo)) * plotW;
    }
    function Y(v) { return top + plotH - ((v - ylo) / (yhi - ylo)) * plotH; }

    /* y gridlines */
    for (var g = 0; g < yTicks.length; g++) {
      var gy = Y(yTicks[g]);
      add(svg, make(doc, 'line', { x1: left, y1: gy, x2: left + plotW, y2: gy, stroke: th.line, 'stroke-width': 1 }));
      text(doc, svg, fmt(yTicks[g]), left - 6, gy + 3.5, { size: tickFs, fill: th.dim, anchor: 'end' });
    }

    /* x ticks: xTicks may be a count, or explicit values / {x,label} entries */
    var xt = [];
    if (typeof o.xTicks === 'number' && isFinite(o.xTicks)) {
      xt = isLog ? logTicks(xlo, xhi) : niceTicks(xlo, xhi, o.xTicks);
      xt = xt.map(function (v) { return { x: v, label: defaultFormat(v) }; });
    } else if (arr(o.xTicks).length) {
      xt = arr(o.xTicks).map(function (v) {
        if (v && typeof v === 'object') {
          var vx = num(v.x, null);
          return isNum(vx) ? { x: vx, label: str(v.label, defaultFormat(vx)) } : null;
        }
        var n2 = num(v, null);
        return isNum(n2) ? { x: n2, label: defaultFormat(n2) } : { x: null, label: str(v) };
      }).filter(function (v) { return v && isNum(v.x); });
    } else {
      xt = (isLog ? logTicks(xlo, xhi) : niceTicks(xlo, xhi, 6)).map(function (v) {
        return { x: v, label: defaultFormat(v) };
      });
    }

    var slotW = xt.length > 1 ? plotW / xt.length : plotW;
    for (var k = 0; k < xt.length; k++) {
      var gx = X(xt[k].x);
      if (gx < left - 0.5 || gx > left + plotW + 0.5) continue;
      add(svg, make(doc, 'line', {
        x1: gx, y1: top, x2: gx, y2: top + plotH, stroke: th.line, 'stroke-width': 1, opacity: 0.7
      }));
      text(doc, svg, xt[k].label, gx, top + plotH + 15, {
        size: 10, fill: th.dim, anchor: 'middle', maxW: Math.max(28, slotW)
      });
    }
    if (xLabel) {
      text(doc, svg, xLabel, left + plotW / 2, H - 4, { size: 10.5, fill: th.dim, anchor: 'middle', maxW: plotW });
    }

    /* vertical marker rule */
    var vline = o.vline;
    if (vline && typeof vline === 'object' && isNum(num(vline.x, null))) {
      var vx = num(vline.x, null);
      var okForAxis = !isLog || vx > 0;
      var px = X(vx);
      if (okForAxis && px >= left - 0.5 && px <= left + plotW + 0.5) {
        add(svg, make(doc, 'line', {
          x1: px, y1: top - 2, x2: px, y2: top + plotH,
          stroke: th.ink, 'stroke-width': 1.25, 'stroke-dasharray': '4 3', opacity: 0.62
        }));
        var vlabel = str(vline.label);
        if (vlabel) {
          var toRight = px < left + plotW * 0.7;
          text(doc, svg, vlabel, px + (toRight ? 5 : -5), top + 8, {
            size: 10, weight: '600', fill: th.ink, anchor: toRight ? 'start' : 'end',
            maxW: toRight ? left + plotW - px - 6 : px - left - 6, tip: vlabel + ' (x = ' + defaultFormat(vx) + ')'
          });
        }
      }
    }

    /* series: paths broken at nulls, then markers */
    for (var si = 0; si < series.length; si++) {
      var s = series[si];
      var d = '', open = false;
      for (var pi = 0; pi < s.points.length; pi++) {
        var pt = s.points[pi];
        if (!isNum(pt.y)) { open = false; continue; } /* gap: do not draw through it */
        d += (open ? ' L' : ' M') + round(X(pt.x)) + ',' + round(Y(pt.y));
        open = true;
      }
      if (d) {
        add(svg, make(doc, 'path', {
          d: d.slice(1), fill: 'none', stroke: s.color, 'stroke-width': 2,
          'stroke-linecap': 'round', 'stroke-linejoin': 'round',
          'stroke-dasharray': s.dashed ? '6 4' : null
        }));
      }
      for (var mi = 0; mi < s.points.length; mi++) {
        var mp = s.points[mi];
        if (!isNum(mp.y)) continue;
        var c = add(svg, make(doc, 'circle', {
          cx: X(mp.x), cy: Y(mp.y), r: 4, fill: s.color,
          stroke: th.card, 'stroke-width': 2 /* 2px surface ring on overlap */
        }));
        tip(doc, c, s.label + '  x=' + defaultFormat(mp.x) + '  y=' + fmt(mp.y));
      }
    }

    if (yLabel) {
      text(doc, svg, yLabel, 0, 0, {
        size: 10.5, fill: th.dim, anchor: 'middle',
        transform: 'translate(' + round(11) + ',' + round(top + plotH / 2) + ') rotate(-90)',
        maxW: plotH
      });
    }
    return svg;
  }

  /* ------------------------------------------------------------------ */
  /* 4. heat                                                             */
  /* ------------------------------------------------------------------ */

  function drawHeat(el, o) {
    var doc = docOf(el), th = theme(el);
    var title = str(o.title);
    var fmt = fmtFn(o.format);
    var nullText = o.nullText === undefined || o.nullText === null ? '—' : str(o.nullText);

    var rows = arr(o.rows).map(function (r, i) {
      return (r && typeof r === 'object') ? str(r.label, 'row ' + (i + 1)) : str(r, 'row ' + (i + 1));
    });
    var cols = arr(o.cols).map(function (c, i) {
      return (c && typeof c === 'object') ? str(c.label, 'col ' + (i + 1)) : str(c, 'col ' + (i + 1));
    });
    var values = arr(o.values);

    if (!rows.length && values.length) {
      for (var r0 = 0; r0 < values.length; r0++) rows.push('row ' + (r0 + 1));
    }
    if (!cols.length && values.length) {
      var maxc = 0;
      for (var c0 = 0; c0 < values.length; c0++) maxc = Math.max(maxc, arr(values[c0]).length);
      for (var c1 = 0; c1 < maxc; c1++) cols.push('col ' + (c1 + 1));
    }
    if (!rows.length || !cols.length) return noData(el, title);

    var flat = [];
    for (var i = 0; i < rows.length; i++) {
      var rowVals = arr(values[i]);
      for (var j = 0; j < cols.length; j++) {
        var v = isNum(rowVals[j]) ? rowVals[j] : num(rowVals[j], null);
        if (isNum(v)) flat.push(v);
      }
    }
    if (!flat.length) return noData(el, title);

    var vmin = isNum(o.min) ? o.min : Math.min.apply(null, flat);
    var vmax = isNum(o.max) ? o.max : Math.max.apply(null, flat);
    if (vmin > vmax) { var sw = vmin; vmin = vmax; vmax = sw; }
    if (vmin === vmax) vmax = vmin + (vmin === 0 ? 1 : Math.abs(vmin));

    var colorLow = str(o.colorLow) || (th.dark ? '#12314f' : '#e7f0fd');
    var colorHigh = str(o.colorHigh) || (th.dark ? '#5598e7' : '#1c5cab');

    /* geometry sized to content; the viewBox scales it to the container */
    var labelFs = 11, cellFs = 11;
    var maxRowLabel = 0;
    for (var rl = 0; rl < rows.length; rl++) maxRowLabel = Math.max(maxRowLabel, estWidth(rows[rl], labelFs));
    var left = clamp(Math.ceil(maxRowLabel) + 10, 60, 220);

    var maxCell = 0;
    for (var f = 0; f < flat.length; f++) maxCell = Math.max(maxCell, estWidth(fmt(flat[f]), cellFs));
    var maxColLabel = 0;
    for (var cl = 0; cl < cols.length; cl++) maxColLabel = Math.max(maxColLabel, estWidth(cols[cl], 10.5));

    /* Keep the nominal width in line with the other charts so that, once the
       viewBox is scaled to the container, type is the same size everywhere. */
    var BASE_W = 760;
    var titleH = title ? TITLE_H : 0;
    var rotate = maxColLabel > Math.max(54, (BASE_W - left - 12) / cols.length) - 6;
    var right = rotate ? clamp(Math.ceil(Math.min(maxColLabel, 150) * 0.71), 12, 110) : 12;
    var cellW = clamp((BASE_W - left - right) / cols.length, 44, 150);
    var cellH = 30;
    var headerH = rotate ? clamp(Math.ceil(Math.min(maxColLabel, 150) * 0.71) + 12, 26, 120) : 20;

    var top = titleH + headerH + 4;
    var W = Math.max(BASE_W, left + cols.length * cellW + right);
    var H = top + rows.length * cellH + 10;

    var svg = makeSvg(el, W, H, title || 'heatmap');
    drawTitle(doc, svg, title, W, th);

    /* column headers */
    for (var ci = 0; ci < cols.length; ci++) {
      var cx = left + cellW * (ci + 0.5);
      if (rotate) {
        var ax = cx, ay = top - 6;
        text(doc, svg, cols[ci], ax, ay, {
          size: 10.5, fill: th.dim, anchor: 'start',
          transform: 'rotate(-45 ' + round(ax) + ' ' + round(ay) + ')',
          maxW: 150, tip: cols[ci]
        });
      } else {
        text(doc, svg, cols[ci], cx, top - 7, {
          size: 10.5, fill: th.dim, anchor: 'middle', maxW: cellW - 4, tip: cols[ci]
        });
      }
    }

    for (var ri = 0; ri < rows.length; ri++) {
      var cy = top + cellH * ri;
      text(doc, svg, rows[ri], left - 8, cy + cellH / 2 + 3.5, {
        size: labelFs, fill: th.ink, anchor: 'end', maxW: left - 12, tip: rows[ri]
      });
      var rowVals2 = arr(values[ri]);
      for (var cj = 0; cj < cols.length; cj++) {
        var raw = rowVals2[cj];
        var val = isNum(raw) ? raw : num(raw, null);
        var x = left + cellW * cj;
        if (!isNum(val)) {
          add(svg, make(doc, 'rect', {
            x: x + 1, y: cy + 1, width: cellW - 2, height: cellH - 2, rx: 3,
            fill: 'none', stroke: th.line, 'stroke-width': 1
          }));
          text(doc, svg, nullText, x + cellW / 2, cy + cellH / 2 + 3.5, {
            size: cellFs, fill: th.dim, anchor: 'middle'
          });
          var hitbox = add(svg, make(doc, 'rect', {
            x: x + 1, y: cy + 1, width: cellW - 2, height: cellH - 2, fill: 'transparent'
          }));
          tip(doc, hitbox, rows[ri] + ' × ' + cols[cj] + ': ' + nullText);
          continue;
        }
        var t = clamp((val - vmin) / (vmax - vmin), 0, 1);
        var fill = mixColor(colorLow, colorHigh, t);
        var cell = add(svg, make(doc, 'rect', {
          x: x + 1, y: cy + 1, width: cellW - 2, height: cellH - 2, rx: 3, fill: fill
        }));
        tip(doc, cell, rows[ri] + ' × ' + cols[cj] + ': ' + fmt(val));
        text(doc, svg, fmt(val), x + cellW / 2, cy + cellH / 2 + 3.5, {
          size: cellFs, weight: '600', fill: readableOn(fill), anchor: 'middle', maxW: cellW - 6
        });
      }
    }
    return svg;
  }

  /* ------------------------------------------------------------------ */
  /* 5. grouped                                                          */
  /* ------------------------------------------------------------------ */

  function drawGrouped(el, o) {
    var doc = docOf(el), th = theme(el);
    var title = str(o.title);
    var fmt = fmtFn(o.yFormat);

    var groups = arr(o.groups).map(function (g, i) {
      return (g && typeof g === 'object') ? str(g.label, 'group ' + (i + 1)) : str(g, 'group ' + (i + 1));
    });
    var series = arr(o.series).filter(function (s) { return s && typeof s === 'object'; }).map(function (s, i) {
      return {
        label: str(s.label, 'series ' + (i + 1)),
        color: seriesColor(el, s.color, i),
        values: arr(s.values).map(function (v) { return isNum(v) ? v : num(v, null); })
      };
    });

    if (!series.length) return noData(el, title);
    if (!groups.length) {
      var maxLen = 0;
      for (var q = 0; q < series.length; q++) maxLen = Math.max(maxLen, series[q].values.length);
      for (var g2 = 0; g2 < maxLen; g2++) groups.push('group ' + (g2 + 1));
    }
    if (!groups.length) return noData(el, title);

    var dmin = 0, dmax = 0, any = false;
    for (var i = 0; i < series.length; i++) {
      for (var j = 0; j < groups.length; j++) {
        var v = series[i].values[j];
        if (!isNum(v)) continue;
        any = true;
        dmin = Math.min(dmin, v);
        dmax = Math.max(dmax, v);
      }
    }
    if (!any) return noData(el, title);
    if (isNum(o.yMax)) dmax = Math.max(dmax, o.yMax);
    if (dmin === dmax) dmax = dmin + 1;

    var W = 760;
    var titleH = title ? TITLE_H : 0;
    var yLabel = str(o.yLabel);
    var ticks = niceTicks(dmin, dmax, 5);
    var lo = Math.min(dmin, ticks[0]);
    var hi = Math.max(dmax, ticks[ticks.length - 1]);
    if (lo === hi) hi = lo + 1;

    var tickFs = 10, maxTickW = 0;
    for (var t = 0; t < ticks.length; t++) maxTickW = Math.max(maxTickW, estWidth(fmt(ticks[t]), tickFs));
    var left = Math.min(120, Math.max(30, maxTickW + 10)) + (yLabel ? 16 : 0);
    var right = 14;
    var plotW = W - left - right;
    var plotH = 250;
    var bottom = 30;

    var svg = makeSvg(el, W, 10, title || 'grouped bar chart');
    var legend = layoutLegend(doc, svg, series.map(function (s) {
      return { label: s.label, color: s.color };
    }), W, th);
    var top = titleH + legend.height + 12;
    var H = top + plotH + bottom;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + round(H));

    drawTitle(doc, svg, title, W, th);
    legend.draw(titleH + 2);

    function Y(v) { return top + plotH - ((v - lo) / (hi - lo)) * plotH; }

    for (var gi = 0; gi < ticks.length; gi++) {
      var gy = Y(ticks[gi]);
      add(svg, make(doc, 'line', { x1: left, y1: gy, x2: left + plotW, y2: gy, stroke: th.line, 'stroke-width': 1 }));
      text(doc, svg, fmt(ticks[gi]), left - 6, gy + 3.5, { size: tickFs, fill: th.dim, anchor: 'end' });
    }
    if (lo < 0) {
      add(svg, make(doc, 'line', { x1: left, y1: Y(0), x2: left + plotW, y2: Y(0), stroke: th.dim, 'stroke-width': 1.25 }));
    }
    if (yLabel) {
      text(doc, svg, yLabel, 0, 0, {
        size: 10.5, fill: th.dim, anchor: 'middle',
        transform: 'translate(' + round(11) + ',' + round(top + plotH / 2) + ') rotate(-90)',
        maxW: plotH
      });
    }

    var bandW = plotW / groups.length;
    var inner = bandW * 0.8;
    var gap = series.length > 1 ? 2 : 0; /* 2px surface gap between adjacent bars */
    var barW = Math.max(2, (inner - gap * (series.length - 1)) / series.length);

    for (var b = 0; b < groups.length; b++) {
      var bx0 = left + bandW * b + (bandW - inner) / 2;
      text(doc, svg, groups[b], left + bandW * (b + 0.5), top + plotH + 16, {
        size: 10.5, fill: th.dim, anchor: 'middle', maxW: bandW - 4
      });
      for (var si = 0; si < series.length; si++) {
        var val = series[si].values[b];
        if (!isNum(val)) continue;
        var x = bx0 + si * (barW + gap);
        var y0 = Y(0), yv = Y(val);
        var yTop = Math.min(y0, yv), barH = Math.max(1, Math.abs(y0 - yv));
        var rect = add(svg, make(doc, 'path', {
          d: barPath(x, yTop, barW, barH, 3, val >= 0 ? 'top' : 'bottom'),
          fill: series[si].color
        }));
        tip(doc, rect, groups[b] + ' — ' + series[si].label + ': ' + fmt(val));
      }
    }
    return svg;
  }

  /* ------------------------------------------------------------------ */
  /* export                                                              */
  /* ------------------------------------------------------------------ */

  var Charts = {
    bar: guard('bar', drawBar),
    stacked: guard('stacked', drawStacked),
    lines: guard('lines', drawLines),
    heat: guard('heat', drawHeat),
    grouped: guard('grouped', drawGrouped),
    /* handy for callers: pass as yFormat */
    formatters: { compact: defaultFormat, percent: pctFormat },
    palette: function (el) { return palette(el || (typeof document !== 'undefined' ? document.body : null)).slice(); },
    version: '1.0.0'
  };

  global.Charts = Charts;
})(typeof window !== 'undefined' ? window : this);
