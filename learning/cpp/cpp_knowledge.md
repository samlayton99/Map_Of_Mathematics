C++ is a compiled language. This means that it takes the code and translates it into assembly. 

C++ is also typed. this means that every declaration of a variable needs to have its corresponding type defined. Objects or aliases that are created, will not infer their type. (note, you can use auto, which will infer it, but it still has to be declared)

Because it is compiled, if you compile and run it, change something, then recompile it, you need to change/delete the binary object if you want it to recompile.

After you compile it, the code will produce an object file for each .cpp file.

The Linker then goes in, combines all .cpp files, all libraries and dependecies, and produces an executable file filename.exe

---
In C++ every variable is either an object or a reference.

An object can have many different forms, can be a constant, a pointer, a regular object, etc.

A reference variable is an alias used with &.

Because of this, whenever I create a new variable that is aliased based off of a previous variable, it doesn't point to the same object, but creates a new object. Variables are objects, not names that alias to objects. 

---
**References** are aliases to previous objects (or variables), and they must be type declared as the same type of the objects they are aliasing. 

References are delcared by adding the "&" at the end of the type. Doing this 

ex:
```
int x = 5; 
int& ref = x; 

//then we do: 
x += 5; ref -= 5; 
std::cout << "x is " << x << ". ref is also " << ref;
```

this would read: x is 5. ref is also 5.

Note that standalone references are not legal (int& r), they must alias something. Also they cannot be re used for other alias. can't be changed later. 

**Pointers**
