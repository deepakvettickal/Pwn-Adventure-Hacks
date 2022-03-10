# P1p2p3

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

## Static analysis by IDA
### Recover function name
`Python version = 3.8`
`file = recover_funcion_name.py`

Use recover_function_name.py in IDA to recover functions' names in IDA.

### Patch mana
`require capstone`
`file = patch_mana.py`

To lock mana, we could patch program. If we need patch lots of pe files, using framework is important. patch_mana.py is a simply script to patch code in GetMana.
## Hacks Instructions

### Teleport Hack
  type the following command when you are running the game.
 this will move player to 1000,1000,1000 (x,y,z) locations
```
teleport 1000,1000,10000
```

### Jump and walk
Using frida to modify value in process to modify speed and hold time.

### Health
Lock health offline model

### Online players' names
Get other players' names (in same map).

### Get enemies' positions
Get enemies' positions
## Authors

Contributors names and contact info

ex. Taranjyot Singh txs153@student.bham.ac.uk  
ex. [@taranjyot95](https://github.com/Taranjyot)

Inspiration, code snippets, etc.
* [Frida Installation guide](https://frida.re/docs/installation/)
* [Javascript API documentation](https://frida.re/docs/javascript-api/)