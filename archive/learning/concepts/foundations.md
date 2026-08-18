Objects are runtime entities. They are core units, but not the most fundamental. Objects consist of:
  - types: what operations/data are valid
  - state/value: its data and what it holds
  - identity: its specific location/id/way to access it
  - lifetime: when it exists and is destroyed

Memory is essentially a running chunk of byte slots and an address for each byte.

so int x = 5; means we will pick a free spot in memory, allocate those slots to the object x, and store the data for 5 (in 0s and 1s) at the memory address. The type is the crucial part, as it tells us how these 0s and 1s are to be interpretted. If it is a float vs an int, the same 0s and 1s will tell us different things. 

It is also important to separate the difference between compile-time and run-time. the types in C++ are only useful in compile time, and completely dissapear after compiled. They essentially are instructions for the compiler of how to interpreta and where to place the data that they represent in the program.

Def: ligature is the thing that takes != and turns it into the not equal signs