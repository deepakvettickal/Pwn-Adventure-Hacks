# Project Title

Pawn Adventure Hacks on Windows By Group 13 

## Description

Implementation of multiple hacks performed using Frida and dll injection.

## Installing
    1. Make sure Pawn Adventure is intalled on your system. 
    2. install Python on windows.
    3. pip install frida-tools // installs frida on windows
    4. pip install cppmangle (Optional if you want to run demangle-exports.py


### Executing program

To run the frida part of the hack use the following command when game is running
```
 python logfile.py 
```

To run demangled-exports.py file to fetch exported functions use 
```
python demangle-exports.py > demangled.txt
```
check demangled.txt for output
## Hacks Instructions

### Teleport Hack
  type the following command when you are running the game.
 this will move player to 1000,1000,1000 (x,y,z) locations
```
teleport 1000,1000,10000
```

## Authors

Contributors names and contact info

ex. Taranjyot Singh txs153@student.bham.ac.uk  
ex. [@taranjyot95](https://github.com/Taranjyot)

Inspiration, code snippets, etc.
* [Frida Installation guide](https://frida.re/docs/installation/)
* [Javascript API documentation](https://frida.re/docs/javascript-api/)