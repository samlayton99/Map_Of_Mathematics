/*
CPP INTRO LAB
-------------
Goal:
Rebuild your C++ foundations from a Python-first perspective.

How to run:
  clang++ -std=c++20 -Wall -Wextra -pedantic learning/cpp_intro.cpp -o cpp_intro
  ./cpp_intro

How to use this file:
1) Read section comments from top to bottom.
2) Run the program after each section.
3) Complete the exercises at the bottom by editing this file.

Why C++ feels different from Python:
- Python: interpreted feel, dynamic typing, garbage collected.
- C++: compiled ahead-of-time, static typing, manual control over memory model.
- C++ gives more control and performance, but asks for more explicit design.
*/

#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

namespace lab {

// SECTION 0: C++ mental model and compile pipeline
// -------------------------------------------------
// You write source code (.cpp files). The compiler translates that into machine code.
// Typical pipeline:
//   source -> preprocessing -> compilation -> linking -> executable
//
// - Compilation checks types and generates object code.
// - Linking resolves symbols from different files/libraries.
//
// This is a key conceptual shift from Python:
// many mistakes are found at compile time instead of runtime.
void lesson0_compile_model() {
    std::cout << "\n[Lesson 0] Compile model\n";
    std::cout << "C++ catches type/interface errors at compile time.\n";
    std::cout << "Compiler + linker produce a native executable.\n";
}

// SECTION 1: Types, variables, and value semantics
// -------------------------------------------------
// In Python, assignment often means "name points to object".
// In C++, assignment usually copies value (unless you use references/pointers/moves).
void lesson1_values_and_types() {
    std::cout << "\n[Lesson 1] Types and values\n";

    int age = 30;
    double pi = 3.14159;
    bool likes_cpp = true;
    std::string name = "Sam";

    std::cout << "name: " << name << ", age: " << age << ", pi: " << pi
              << ", likes_cpp: " << std::boolalpha << likes_cpp << "\n";

    int a = 5;
    int b = a; // copy by value
    b = 99;
    std::cout << "a stays " << a << ", b changed to " << b
              << " (copy semantics)\n";
}

// SECTION 2: References vs pointers (core concept)
// -------------------------------------------------
// Reference (int&):
// - Alias to an existing object.
// - Must be initialized when created.
// - Cannot be reseated to alias a different object.
//
// Pointer (int*):
// - Stores an address.
// - Can be null.
// - Can be reseated to point somewhere else.
// - Dereference with *ptr to access value.
void lesson2_references_and_pointers() {
    std::cout << "\n[Lesson 2] References and pointers\n";

    int x = 10;
    int y = 50;

    int& ref = x; // ref aliases x
    ref += 5;
    std::cout << "x after ref += 5: " << x << "\n";

    int* ptr = &x; // ptr holds address of x
    *ptr += 20;    // dereference and modify x
    std::cout << "x after *ptr += 20: " << x << "\n";

    ptr = &y;      // reseat pointer to y
    *ptr += 7;
    std::cout << "y after reseated pointer: " << y << "\n";

    // Memory intuition:
    // x lives at an address. &x gets address. ptr stores that address.
    // *ptr means "go to that address and read/write the value there."
}

// SECTION 3: Stack, heap, and RAII
// ---------------------------------
// Stack:
// - Automatic storage (local variables). Fast lifetime management.
// - Lifetime usually tied to scope.
//
// Heap:
// - Dynamic storage (requested at runtime).
// - In modern C++, prefer smart pointers (std::unique_ptr/std::shared_ptr)
//   over raw new/delete.
//
// RAII = Resource Acquisition Is Initialization.
// Resource ownership is tied to object lifetime.
// Constructor acquires, destructor releases automatically.
struct Tracer {
    explicit Tracer(std::string label) : label_(std::move(label)) {
        std::cout << "Tracer(" << label_ << ") constructed\n";
    }
    ~Tracer() {
        std::cout << "Tracer(" << label_ << ") destructed\n";
    }
private:
    std::string label_;
};

void lesson3_memory_and_raii() {
    std::cout << "\n[Lesson 3] Stack, heap, and RAII\n";

    {
        Tracer stack_obj("stack");
        std::cout << "Inside scope with stack object.\n";
    } // destructor runs here automatically

    auto heap_obj = std::make_unique<Tracer>("heap(unique_ptr)");
    std::cout << "Heap object managed by unique_ptr.\n";
    // No delete needed: unique_ptr frees resource automatically.

    // If you use raw pointers + new/delete, you must manually delete,
    // and mistakes cause leaks/dangling pointers.
}

// SECTION 4: Containers and strings
// ---------------------------------
// Prefer std::vector and std::string over C-style arrays/char* for most tasks.
// They own memory and manage resizing/lifetime safely.
void lesson4_standard_library_basics() {
    std::cout << "\n[Lesson 4] std::vector and std::string\n";

    std::vector<int> nums{1, 2, 3};
    nums.push_back(4);

    int sum = 0;
    for (int n : nums) {
        sum += n;
    }
    std::cout << "sum of nums = " << sum << "\n";

    std::string s = "C++";
    s += " from Python";
    std::cout << "message: " << s << "\n";
}

// SECTION 5: Functions, const correctness, and API design
// --------------------------------------------------------
// const is a contract: "I will not modify this through this interface."
// Use const references for read-only access without copying.
int squared(int x) {
    return x * x;
}

void print_name_upper_hint(const std::string& name) {
    // name is read-only here because of const&
    std::cout << "Name length is " << name.size() << "\n";
}

void lesson5_functions_and_const() {
    std::cout << "\n[Lesson 5] Functions and const correctness\n";
    std::cout << "7 squared = " << squared(7) << "\n";
    print_name_upper_hint("samlayton");
}

// SECTION 6: Common C++ footguns to avoid
// ---------------------------------------
// 1) Dangling pointers/references:
//    pointer/reference outlives the object it points to.
// 2) Manual memory management errors:
//    leaks, double-delete, use-after-free.
// 3) Undefined behavior:
//    program may appear to work, then fail unpredictably.
//
// Best beginner strategy:
// - Prefer value types.
// - Prefer std containers.
// - Prefer smart pointers when dynamic allocation is required.
// - Compile with warnings enabled and treat warnings seriously.
void lesson6_footguns() {
    std::cout << "\n[Lesson 6] Footguns and safety habits\n";
    std::cout << "Use value semantics + RAII + std containers first.\n";
    std::cout << "Reach for raw pointers mainly for non-owning references.\n";
}

} // namespace lab

int main() {
    std::cout << "=== C++ Intro Lab (Python -> C++) ===\n";

    lab::lesson0_compile_model();
    lab::lesson1_values_and_types();
    lab::lesson2_references_and_pointers();
    lab::lesson3_memory_and_raii();
    lab::lesson4_standard_library_basics();
    lab::lesson5_functions_and_const();
    lab::lesson6_footguns();

    std::cout << "\nExercises (edit this file and rerun):\n";
    std::cout << "1) Write a function: int cube(int x)\n";
    std::cout << "2) Create a vector of 5 ints and print average\n";
    std::cout << "3) Make a function that swaps two ints using references\n";
    std::cout << "4) Make a heap object with unique_ptr and explain ownership\n";
    std::cout << "5) Add one example of const correctness in your own code\n";

    return 0;
}
