# Brainfuck Compiler (BFC)
Python-based Brainfuck compiler and interpreter.

## Samples
- You can explore the provided sample programs [here](examples/)

## Features
- Compiles Brainfuck to an executable OR C++ source
- Supports preprocessing
- Generates standalone executables

## Usage
'bfc.py <INPUT_FILE> [-h] [-o OUTPUT_FILE] [-p] [-v] [--allow-loop-extension] [--do-not-optimize] [--show-w] [--show-c]'

## Dependencies
- Python 3.10+
- ply library for lexer/parser
- g++ compiler (currently only supports g++)

## Better BF format
- Optional syntactic sugar for bf
```cpp
Original:
+++++[------]

Revised:
+5[-6]
```
(use --allow-loop-extension as a command line argument to allow this behaviour on loops ('[' & ']'))
