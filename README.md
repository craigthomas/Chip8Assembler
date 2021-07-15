# (Super) Chip 8 Assembler

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/craigthomas/Chip8Assembler/Build%20Test%20Coverage?style=flat-square)](https://github.com/craigthomas/Chip8Assembler/actions)
[![Codecov](https://img.shields.io/codecov/c/gh/craigthomas/Chip8Assembler?style=flat-square)](https://codecov.io/gh/craigthomas/Chip8Assembler) 
[![Dependencies](https://img.shields.io/librariesio/github/craigthomas/Chip8Assembler?style=flat-square)](https://libraries.io/github/craigthomas/Chip8Assembler)
[![Releases](https://img.shields.io/github/release/craigthomas/Chip8Python?style=flat-square)](https://github.com/craigthomas/Chip8Python/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)

## Table of Contents

1. [What is it?](#what-is-it)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
    1. [Input Format](#input-format)
    2. [Print Symbol Table](#print-symbol-table)
    3. [Print Assembled Statements](#print-assembled-statements)
5. [Mnemonic Table](#mnemonic-table)
    1. [Chip 8 Mnemonics](#chip-8-mnemonics)
    2. [Super Chip 8 Mnemonics](#super-chip-8-mnemonics)
    3. [Pseudo Operations](#pseudo-operations)
    4. [Operands](#operands)
6. [License](#license)
7. [Further Documentation](#further-documentation)

## What is it?

This project is a (Super) Chip 8 assembler written in Python 3.6. The assembler will
take valid Super Chip 8 assembly statements and generate a binary file containing
the correct machine instructions.


## Requirements

In order to run the assembler, you will need to use Python 3.6 or greater. If you wish
to clone the repository for development, you will need Git.


## Installation

To install the source files, download the latest release from the 
[releases](https://github.com/craigthomas/Chip8Assembler/releases) section of 
the repository and unzip the contents in a directory of your choice. Or, 
clone the repository in the directory of your choice with:

    git clone https://github.com/craigthomas/Chip8Assembler.git
    
Next, you will need to install the required packages for the file:

    pip install -r requirements.txt


## Usage

To run the assembler:

    python assembler.py input_file --output output_file

This will assemble the instructions found in file `input_file` and will generate
the associated Chip 8 machine instructions in binary format in `output_file`.

### Input Format

The input file needs to follow the format below:

    LABEL    MNEMONIC    OPERANDS    COMMENT

Where:

* `LABEL` is a 15 character label for the statement
* `MNEMONIC` is a Chip 8 operation mnemonic from the [Mnemonic Table](#mnemonic-table) below
* `OPERANDS` are registers, values or labels, as described in the [Operands](#operands) section
* `COMMENT` is a 30 character comment describing the statement (may have a `#` preceding it)

An example file:

    # A comment line that contains nothing
    clear    CLR
    start    LOAD    r1,$0     Clear contents of register 1
             ADD     r1,$1     Add 1 to the register
             SKE     r1,$A     Check to see if we are at 10
             JUMP    start     Jump back to the start
    end      JUMP    end       Loop forever
    data     FCB     $1A       One byte piece of data
    data1    FDB     $FBEE     Two byte piece of data


### Print Symbol Table

To print the symbol table that is generated during assembly, use the `--symbols` 
switch:

    python assembler.py test.asm --symbols

Which will have the following output:

    -- Symbol Table --
    0x0200 clear
    0x0202 start
    0x020A end
    0x020C data
    0x020E data1


### Print Assembled Statements

To print out the assembled version of the program, use the `--print` switch:

    python assembler.py test.asm --print

Which will have the following output:

    -- Assembled Statements --
    0x0200 0000                                   # A comment line that contains nothing    
    0x0200 00E0      clear   CLR                  #                                         
    0x0202 6100      start  LOAD           r1,$0  # Clear contents of register 1            
    0x0204 7101              ADD           r1,$1  # Add 1 to the register                   
    0x0206 310A              SKE           r1,$A  # Check to see if we are at 10            
    0x0208 1202             JUMP           start  # Jump back to the start                  
    0x020A 120A        end  JUMP             end  # Loop forever                            
    0x020C 001A       data   FCB             $1A  # One byte piece of data                  
    0x020E FBEE      data1   FDB           $FBEE  # Two byte piece of data           

With this output, the first column is the offset in hex where the statement starts,
the second column contains the full machine-code operand, the third column is the
user-supplied label for the statement, the forth column is the mnemonic, the fifth
column is the register values of other numeric or label data the operation will
work on, and the fifth column is the comment string.


## Mnemonic Table

The assembler supports mnemonics for both the Chip 8 and Super Chip 8 language
specifications, as well as pseudo operations.

### Chip 8 Mnemonics

| Mnemonic | Opcode | Operands | Description |
| -------- | ------ | :------: | ----------- |
| `SYS`    | `0nnn` | 1 | System call (ignored)                                          |
| `CLR`    | `00E0` | 0 | Clear the screen                                               |
| `RTS`    | `00EE` | 0 | Return from subroutine                                         |
| `JUMP`   | `1nnn` | 1 | Jump to address `nnn`                                          |
| `CALL`   | `2nnn` | 1 | Call routine at address `nnn`                                  |
| `SKE`    | `3snn` | 2 | Skip next instruction if register `s` equals `nn`              |
| `SKNE`   | `4snn` | 2 | Do not skip next instruction if register `s` equals `nn`       |
| `SKRE`   | `5st0` | 2 | Skip if register `s` equals register `t`                       |
| `LOAD`   | `6snn` | 2 | Load register `s` with value `nn`                              |
| `ADD`    | `7snn` | 2 | Add value `nn` to register `s`                                 |
| `MOVE`   | `8st0` | 2 | Move value from register `s` to register `t`                   |
| `OR`     | `8st1` | 2 | Perform logical OR on register `s` and `t` and store in `t`    |
| `AND`    | `8st2` | 2 | Perform logical AND on register `s` and `t` and store in `t`   |
| `XOR`    | `8st3` | 2 | Perform logical XOR on register `s` and `t` and store in `t`   |
| `ADDR`   | `8st4` | 2 | Add `s` to `t` and store in `s` - register `F` set on carry    |
| `SUB`    | `8st5` | 2 | Subtract `s` from `t` and store in `s` - register `F` set on !borrow         |
| `SHR`    | `8st6` | 2 | Shift bits in `s` 1 bit right, store in `t` - bit 0 shifts to register `F` |
| `SHL`    | `8stE` | 2 | Shift bits in `s` 1 bit left, store in `t` - bit 7 shifts to register `F`  |
| `SKRNE`  | `9st0` | 2 | Skip next instruction if register `s` not equal register `t`   |
| `LOADI`  | `Annn` | 1 | Load index with value `nnn`                                    |
| `JUMPI`  | `Bnnn` | 1 | Jump to address `nnn` + index                                  |
| `RAND`   | `Ctnn` | 2 | Generate random number between 0 and `nn` and store in `t`     |
| `DRAW`   | `Dstn` | 3 | Draw `n` byte sprite at x location reg `s`, y location reg `t` |
| `SKPR`   | `Es9E` | 1 | Skip next instruction if the key in reg `s` is pressed         |
| `SKUP`   | `EsA1` | 1 | Skip next instruction if the key in reg `s` is not pressed     |
| `MOVED`  | `Ft07` | 1 | Move delay timer value into register `t`                       |
| `KEYD`   | `Ft0A` | 1 | Wait for keypress and store in register `t`                    |
| `LOADD`  | `Fs15` | 1 | Load delay timer with value in register `s`                    |
| `LOADS`  | `Fs18` | 1 | Load sound timer with value in register `s`                    |
| `ADDI`   | `Fs1E` | 1 | Add value in register `s` to index                             |
| `LDSPR`  | `Fs29` | 1 | Load index with sprite from register `s`                       |
| `BCD`    | `Fs33` | 1 | Store the binary coded decimal value of register `s` at index  |
| `STOR`   | `Fs55` | 1 | Store the values of register `s` registers at index            |
| `READ`   | `Fs65` | 1 | Read back the stored values at index into registers            |

### Super Chip 8 Mnemonics

| Mnemonic | Opcode | Operands | Description |
| -------- | ------ | :------: | ----------- |
| `SCRD`   | `00Cn` | 1 | Scroll down `n` lines                                          |
| `SCRR`   | `00FB` | 0 | Scroll right 4 pixels                                          |
| `SCRL`   | `00FC` | 0 | Scroll left 4 pixels                                           |
| `EXIT`   | `00FD` | 0 | Exit interpreter                                               |
| `EXTD`   | `00FE` | 0 | Disable extended mode                                          |
| `EXTE`   | `00FF` | 0 | Enable extended mode                                           |
| `SRPL`   | `Fs75` | 1 | Store subset of registers in RPL store                         |
| `LRPL`   | `Fs85` | 1 | Read back subset of registers from RPL store                   |

### Pseudo Operations

| Mnemonic | Description |
| -------- | ----------- |
| `FCB`    | Defines a single byte constant value |
| `FDB`    | Defines a double byte constant value |

Both `FCB` and `FDB` should be defined at the end of your program, otherwise they will be interpreted as program code.


### Operands

Operands may be one of three different types:

| Operand Type | Example | Description |
| ------------ | :-----: | ----------- |
| Register     | `r4`    | Valid registers are in the range 0-F and must start with an `r` or `R` |
| Hex value    | `$1234` | Specifies a hexadecimal value. Must begin with a `$`.                  |
| Label        | `start` | Labels may be any string as long as it is not `r1` - `rF`              |


## License

Please see the file called `LICENSE`.


## Further Documentation

The best documentation is in the code itself. Please feel free to examine the
code and experiment with it. 
