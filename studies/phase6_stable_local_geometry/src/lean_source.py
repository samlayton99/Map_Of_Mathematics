#!/usr/bin/env python3
"""Locate a Lean declaration's source text in the corpus checkout.

Given a fully-qualified declaration name and its module (from
/Users/sam/mathmap_data/all_modules.tsv) this finds the declaration header
(its STATEMENT) and, optionally, the body/proof source.

Resolution is purely textual. Every file is indexed once, keyed by the fully
qualified name built from the namespace/section stack plus the declared name.
Five extra sources of names are indexed because Mathlib generates a large
fraction of its declarations rather than writing them:

  * structure/class fields and inductive constructors (projections);
  * `extends` parents (`class Preorder extends LE a` -> `Preorder.toLE`);
  * explicit targets of `@[to_dual X]` / `@[to_additive X]`;
  * anonymous `instance : C ...` blocks, matched by Lean's `inst<C>...` name;
  * `alias X := Y`.
"""
import os
import re

MATHLIB = "/Users/sam/my-repos/research/Map_Of_Mathematics/corpusenv/mathlib"
TOOLCHAIN_SRC = os.path.expanduser(
    "~/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean")
PKGS = os.path.join(MATHLIB, ".lake", "packages")

ROOT_DIRS = {
    "Mathlib": MATHLIB,
    "Archive": MATHLIB,
    "Counterexamples": MATHLIB,
    "Init": TOOLCHAIN_SRC,
    "Lean": TOOLCHAIN_SRC,
    "Std": TOOLCHAIN_SRC,
    "Lake": TOOLCHAIN_SRC,
    "Batteries": os.path.join(PKGS, "batteries"),
    "Aesop": os.path.join(PKGS, "aesop"),
    "Qq": os.path.join(PKGS, "Qq"),
    "Plausible": os.path.join(PKGS, "plausible"),
    "ProofWidgets": os.path.join(PKGS, "proofwidgets"),
    "LeanSearchClient": os.path.join(PKGS, "LeanSearchClient"),
    "ImportGraph": os.path.join(PKGS, "importGraph"),
    "Cli": os.path.join(PKGS, "Cli"),
}

MODIFIERS = ("private", "protected", "noncomputable", "partial", "unsafe",
             "nonrec", "scoped", "local", "irreducible")
KEYWORDS = ("theorem", "lemma", "def", "abbrev", "instance", "structure",
            "class", "inductive", "opaque", "axiom", "alias")

_MODS = r"(?:(?:%s)\s+)*" % "|".join(MODIFIERS)
DECL_RE = re.compile(r"^" + _MODS + r"(?P<kw>%s)\b(?P<rest>.*)$"
                     % "|".join(KEYWORDS))
NS_RE = re.compile(r"^namespace\s+(\S+)")
SEC_RE = re.compile(r"^section\b\s*(\S+)?")
END_RE = re.compile(r"^end\b\s*(\S+)?")
NAME_RE = re.compile(r"^\s*([^\s:({\[⟨,{}]+)")
PRIO_RE = re.compile(r"^\s*\((?:priority|prio)\s*:=[^)]*\)")
FIELD_RE = re.compile(r"^\s+(?:@\[[^\]]*\]\s*)?(?:protected\s+)?"
                      r"([A-Za-z_][^\s:({\[⟨,]*)\s*:")
CTOR_RE = re.compile(r"^\s*\|\s*([A-Za-z_][^\s:({\[⟨,]*)")
EXTENDS_RE = re.compile(r"\bextends\b(?P<body>[^:]*?)(?=\swhere\b|:=|:\s|$)",
                        re.S)
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.'!?]*")
TRANSLATE_ATTR_RE = re.compile(
    r"\b(?:to_dual|to_additive)\b(?P<args>[^,\]]*)")
PRIVATE_RE = re.compile(r"^_private\.[^.]+(?:\.[^.]+)*?\.\d+\.(.*)$")

OPENERS = "([{⟨"
CLOSERS = ")]}⟩"


def module_path(module):
    root = (module or "").split(".")[0]
    base = ROOT_DIRS.get(root)
    if base is None:
        return None
    p = os.path.join(base, *module.split(".")) + ".lean"
    return p if os.path.exists(p) else None


def _attr_end(s, depth=0, start=0):
    """Index just past the ']' closing an attribute block starting at `start`."""
    i = start
    while i < len(s):
        if s[i] == "[":
            depth += 1
        elif s[i] == "]":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(s)


def _strip_comments(lines):
    """Same lines with block and line comments blanked out (positions kept)."""
    out, depth = [], 0
    for ln in lines:
        res, j, n = [], 0, len(ln)
        while j < n:
            two = ln[j:j + 2]
            if depth > 0:
                if two == "/-":
                    depth += 1
                    j += 2
                elif two == "-/":
                    depth -= 1
                    j += 2
                else:
                    j += 1
                continue
            if two == "/-":
                depth += 1
                j += 2
                continue
            if two == "--":
                break
            res.append(ln[j])
            j += 1
        out.append("".join(res))
    return out


def _comment_mask(lines):
    """True where the line begins inside a block comment."""
    mask = [False] * len(lines)
    depth = 0
    for i, ln in enumerate(lines):
        mask[i] = depth > 0
        j, n = 0, len(ln)
        while j < n - 1:
            two = ln[j:j + 2]
            if depth == 0 and two == "--":
                break
            if two == "/-":
                depth += 1
                j += 2
                continue
            if two == "-/":
                depth = max(0, depth - 1)
                j += 2
                continue
            j += 1
    return mask


def _split_body(text):
    """Split at the first top-level ':=' or 'where'. Returns (stmt, body)."""
    depth, i, n, in_str = 0, 0, len(text), False
    while i < n:
        c = text[i]
        if in_str:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            i += 1
            continue
        if text[i:i + 2] == "--":
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if text[i:i + 2] == "/-":
            j = text.find("-/", i)
            i = n if j < 0 else j + 2
            continue
        if c in OPENERS:
            depth += 1
        elif c in CLOSERS:
            depth = max(0, depth - 1)
        elif depth == 0:
            if text[i:i + 2] == ":=":
                return text[:i].rstrip(), text[i:]
            if text.startswith("where", i) and (i == 0 or not (
                    text[i - 1].isalnum() or text[i - 1] == "_")):
                if text[i + 5:i + 6] in ("", " ", "\n", "\t"):
                    return text[:i].rstrip(), text[i:]
        i += 1
    return text.rstrip(), ""


class FileIndex:
    """full-name -> (start_line, end_line) for one .lean file."""

    def __init__(self, path):
        with open(path, encoding="utf-8", errors="replace") as f:
            self.lines = f.read().split("\n")
        self.decls = {}      # exact names written or predictably generated
        self.anon = []       # (ns, class_head, start, end) anonymous instances
        self._build()

    # -------------------------------------------------------------- build
    def _build(self):
        lines = self.lines
        cmask = _comment_mask(lines)
        col0 = {i for i, ln in enumerate(lines)
                if ln and not ln[0].isspace() and not cmask[i]}

        def block_end(i):
            j = i + 1
            while j < len(lines) and j not in col0:
                j += 1
            return j

        code = _strip_comments(lines)
        stack, attrs, attr_open, attr_age = [], "", 0, 0
        for i in range(len(lines)):
            ln = code[i].rstrip()
            if attr_open > 0:
                attr_age += 1
                if attr_age > 20:            # runaway guard
                    attrs, attr_open = "", 0
                    continue
                prev = attr_open
                attr_open += ln.count("[") - ln.count("]")
                if attr_open > 0:
                    attrs += "\n" + ln
                    continue
                cut = _attr_end(ln, depth=prev)
                attrs += "\n" + ln[:cut]
                ln = ln[cut:].lstrip()
                if not ln:
                    continue
            elif not ln or ln[0].isspace():
                continue
            if ln.startswith("@["):
                bal = ln.count("[") - ln.count("]")
                if bal > 0:
                    attrs, attr_open, attr_age = ln, bal, 0
                    continue
                cut = _attr_end(ln)
                attrs, ln = ln[:cut], ln[cut:].lstrip()
                if not ln:
                    continue

            m = NS_RE.match(ln)
            if m:
                stack.append(("ns", m.group(1)))
                attrs = ""
                continue
            m = END_RE.match(ln)
            if m:
                nm = m.group(1)
                if nm:
                    for j in range(len(stack) - 1, -1, -1):
                        if stack[j][1] == nm:
                            del stack[j:]
                            break
                    else:
                        if stack:
                            stack.pop()
                elif stack:
                    stack.pop()
                attrs = ""
                continue
            m = SEC_RE.match(ln)
            if m:
                stack.append(("sec", m.group(1)))
                attrs = ""
                continue

            m = DECL_RE.match(ln)
            if not m:
                # inline `@[...] theorem foo ...` on one line
                m2 = re.match(r"^@\[.*?\]\s*(.*)$", ln)
                if m2:
                    m = DECL_RE.match(m2.group(1))
                    if m:
                        attrs = ln[:len(ln) - len(m2.group(1))]
                if not m:
                    attrs = ""
                    continue

            ns = ".".join(s[1] for s in stack if s[0] == "ns")
            kw, rest = m.group("kw"), m.group("rest")
            if kw == "class" and re.match(r"\s+inductive\b", rest):
                kw, rest = "inductive", rest[rest.index("inductive") + 9:]
            if kw == "instance":
                pm = PRIO_RE.match(rest)
                if pm:
                    rest = rest[pm.end():]
            nm = NAME_RE.match(rest)
            name = nm.group(1) if nm else None
            if name in ("|", "where", "extends", "|"):
                name = None
            end = block_end(i)

            if name is None:
                if kw == "instance":
                    head = self._class_head(rest)
                    if head:
                        self.anon.append((ns, head, i, end))
                attrs = ""
                continue

            if name.startswith("_root_."):
                full = name[len("_root_."):]
            else:
                full = f"{ns}.{name}" if ns else name
            self.decls.setdefault(full, (i, end))

            # generated siblings named explicitly in the attribute block
            for am in TRANSLATE_ATTR_RE.finditer(attrs):
                for tok in IDENT_RE.findall(
                        re.sub(r"/-.*?-/", " ", am.group("args"), flags=re.S)):
                    if tok in ("attr", "simp", "existing", "reorder", "self",
                               "norm_cast", "elab_as_elim", "gcongr", "push",
                               "grind", "mono", "aesop", "bound", "measurability",
                               "fun_prop", "simps", "deprecated", "since"):
                        continue
                    alias = tok if "." in tok or not ns else f"{ns}.{tok}"
                    self.decls.setdefault(alias, (i, end))
                    self.decls.setdefault(tok, (i, end))

            if kw in ("structure", "class", "inductive"):
                self._index_members(full, i, end, kw)
            attrs = ""

    @staticmethod
    def _class_head(rest):
        """`instance : Category C where` -> 'Category' (last component)."""
        depth = 0
        for i, c in enumerate(rest):
            if c in OPENERS:
                depth += 1
            elif c in CLOSERS:
                depth = max(0, depth - 1)
            elif c == ":" and depth == 0 and rest[i:i + 2] != ":=":
                m = IDENT_RE.search(rest[i + 1:])
                return m.group(0).split(".")[-1] if m else None
        return None

    def _index_members(self, parent, start, end, kw):
        header = "\n".join(self.lines[start:end])
        stmt, _ = _split_body(header)
        em = EXTENDS_RE.search(stmt)
        if em:
            for part in em.group("body").split(","):
                im = IDENT_RE.search(part)
                if im:
                    p = im.group(0).rstrip(".").split(".")[-1]
                    if p:
                        self.decls.setdefault(f"{parent}.to{p}", (start, end))
        if kw != "inductive":
            self.decls.setdefault(f"{parent}.mk", (start, end))
            cm = re.search(r"^\s*([A-Za-z_][\w'!?]*)\s*::", header, re.M)
            if cm:
                self.decls.setdefault(f"{parent}.{cm.group(1)}", (start, end))
        for k in range(start + 1, end):
            ln = self.lines[k]
            if not ln.strip():
                continue
            m = CTOR_RE.match(ln) if kw == "inductive" else FIELD_RE.match(ln)
            if m:
                self.decls.setdefault(f"{parent}.{m.group(1)}", (k, k + 1))

    # ------------------------------------------------------------- lookup
    def get(self, full):
        hit = self.decls.get(full)
        if hit:
            return hit, "exact"
        keys = [k for k in self.decls
                if k.endswith("." + full) or full.endswith("." + k)]
        if len(keys) == 1:
            return self.decls[keys[0]], "suffix"
        last = full.split(".")[-1]
        keys = [k for k in self.decls if k.split(".")[-1] == last]
        if len(keys) == 1:
            return self.decls[keys[0]], "lastcomp"
        # anonymous instance: Lean names it `inst<Class><Type...>`
        ns, _, base = full.rpartition(".")
        if base.startswith("inst"):
            hits = [(s, e) for (a_ns, head, s, e) in self.anon
                    if (a_ns == ns or not ns or not a_ns)
                    and base.startswith("inst" + head)]
            if len(hits) == 1:
                return hits[0], "anon-instance"
            hits = [(s, e) for (a_ns, head, s, e) in self.anon
                    if base.startswith("inst" + head)]
            if len(hits) == 1:
                return hits[0], "anon-instance"
        return None, None


# --------------------------------------------------------------------------
# Mathlib writes one declaration and generates its sibling. `@[to_additive]`
# and `@[to_dual]` without an explicit name leave nothing in the file under
# the generated name, so we translate the generated name back to the one that
# was actually written and resolve THAT, in the same file. Purely a source
# retrieval device: the brief says which original it came from.
_ADD2MUL_CAMEL = {"Add": "Mul", "Zero": "One", "Neg": "Inv", "Sub": "Div",
                  "Sum": "Prod", "VAdd": "SMul", "NSMul": "NPow",
                  "ZSMul": "ZPow", "Additive": "Multiplicative"}
_ADD2MUL_SNAKE = {"add": "mul", "zero": "one", "neg": "inv", "sub": "div",
                  "sum": "prod", "nsmul": "npow", "zsmul": "zpow",
                  "vadd": "smul", "smul": "pow"}
_DUAL = {"iInf": "iSup", "iSup": "iInf", "sInf": "sSup", "sSup": "sInf",
         "inf": "sup", "sup": "inf", "Inf": "Sup", "Sup": "Inf",
         "top": "bot", "bot": "top", "Top": "Bot", "Bot": "Top",
         "min": "max", "max": "min", "Min": "Max", "Max": "Min"}
_CAMEL_RE = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z0-9'!?]*|[a-z0-9'!?]+")


def _variants(component):
    """Plausible written names for one dot-component of a generated name."""
    out = []
    snake = component.split("_")
    if any(t in _ADD2MUL_SNAKE for t in snake):
        out.append("_".join(_ADD2MUL_SNAKE.get(t, t) for t in snake))
    if any(t in _DUAL for t in snake):
        d = [_DUAL.get(t, t) for t in snake]
        out.append("_".join(d))
        out.append("_".join(reversed(d)))
    camel = _CAMEL_RE.findall(component)
    if camel and any(t in _ADD2MUL_CAMEL for t in camel):
        out.append("".join(_ADD2MUL_CAMEL.get(t, t) for t in camel))
    if len(camel) > 1 and camel[0] == "Add":
        out.append("".join(camel[1:]))
        out.append("".join(_ADD2MUL_CAMEL.get(t, t) for t in camel[1:]))
    if component.startswith("to") and len(camel) > 2 and camel[1] == "Add":
        out.append("to" + "".join(camel[2:]))
    return [v for v in out if v and v != component]


def translated_names(full):
    """Candidate written names for a `to_additive` / `to_dual` output."""
    parts = full.split(".")
    seen, out = set(), []
    for i, p in enumerate(parts):
        for v in _variants(p):
            cand = ".".join(parts[:i] + [v] + parts[i + 1:])
            if cand not in seen:
                seen.add(cand)
                out.append(cand)
    # translate every component at once (class hierarchies need this)
    allv = ".".join(_variants(p)[0] if _variants(p) else p for p in parts)
    if allv != full and allv not in seen:
        out.append(allv)
    return out


_CACHE = {}


def get_index(path):
    if path not in _CACHE:
        _CACHE[path] = FileIndex(path)
    return _CACHE[path]


def _dedent(text):
    lines = text.split("\n")
    body = [l for l in lines if l.strip()]
    if not body:
        return text
    pad = min(len(l) - len(l.lstrip()) for l in body)
    return "\n".join(l[pad:] if len(l) >= pad else l for l in lines)


def lookup(name, module, max_stmt_lines=20, max_body_lines=40, want_body=False):
    """Return {'statement','body','how'} or None if the source is not found."""
    path = module_path(module)
    if path is None:
        return None
    try:
        idx = get_index(path)
    except OSError:
        return None

    cand = name
    m = PRIVATE_RE.match(name)
    if m:
        cand = m.group(1)

    hit, how = idx.get(cand)
    source_name = None
    if hit is None:
        for v in translated_names(cand):
            h2 = idx.decls.get(v)
            if h2 is not None:
                hit, how, source_name = h2, "translated", v
                break
    if hit is None:
        # `@[simps]` / `@[reassoc]` projections: fall back to the declaration
        # they were generated from, by dropping trailing name components.
        parts = cand.split(".")
        base, tail = ".".join(parts[:-1]), parts[-1].split("_")
        for k in range(len(tail) - 1, max(0, len(tail) - 4), -1):
            v = (base + "." if base else "") + "_".join(tail[:k])
            h2 = idx.decls.get(v)
            if h2 is not None:
                hit, how, source_name = h2, "generated-from", v
                break
    if hit is None:
        return None

    s, e = hit
    block = "\n".join(idx.lines[s:e]).rstrip()
    stmt, body = _split_body(block)
    stmt = _dedent(stmt).strip("\n")
    sl = stmt.split("\n")
    truncated = len(sl) > max_stmt_lines
    if truncated:
        stmt = "\n".join(sl[:max_stmt_lines]) + "\n  -- ..."
    out = {"statement": stmt, "how": how, "body": None,
           "source_name": source_name}
    if want_body:
        body = _dedent(body).strip("\n")
        if body:
            bl = body.split("\n")
            if len(bl) > max_body_lines:
                body = "\n".join(bl[:max_body_lines]) + "\n  -- ..."
            out["body"] = body
    return out
