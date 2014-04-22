'''
Copyright (C) 2014 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

A Chip 8 assembler - see the README.md file for details.
'''
# I M P O R T S ###############################################################

import argparse
import re
import sys

# C O N S T A N T S ###########################################################

LABEL = "label"
OP = "op"
OPERANDS = "operands"
COMMENT = "comment"
SOURCE = "source"
TARGET = "target"
NUMERIC = "numeric"

# Opcode translation
OPERATIONS = {
    "SYS"  : { OP: "0nnn", OPERANDS: 1, SOURCE: 0, TARGET: 0, NUMERIC: 3 },
    "JUMP" : { OP: "1nnn", OPERANDS: 1, SOURCE: 0, TARGET: 0, NUMERIC: 3 },
    "CALL" : { OP: "2nnn", OPERANDS: 1, SOURCE: 0, TARGET: 0, NUMERIC: 3 },
    "SKE"  : { OP: "3snn", OPERANDS: 2, SOURCE: 1, TARGET: 0, NUMERIC: 2 },
    "SKNE" : { OP: "4snn", OPERANDS: 2, SOURCE: 1, TARGET: 0, NUMERIC: 2 },
    "SKRE" : { OP: "5stn", OPERANDS: 3, SOURCE: 1, TARGET: 1, NUMERIC: 1 },
    "LOAD" : { OP: "6snn", OPERANDS: 2, SOURCE: 1, TARGET: 0, NUMERIC: 2 },
    "ADD"  : { OP: "7snn", OPERANDS: 2, SOURCE: 1, TARGET: 0, NUMERIC: 2 },
    "MOVE" : { OP: "8st0", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "OR"   : { OP: "8st1", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "AND"  : { OP: "8st2", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "XOR"  : { OP: "8st3", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "ADDR" : { OP: "8st4", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "SUB"  : { OP: "8st5", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "SHR"  : { OP: "8st6", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "SUBN" : { OP: "8st7", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "SHL"  : { OP: "8stE", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "SKRNE": { OP: "9st0", OPERANDS: 2, SOURCE: 1, TARGET: 1, NUMERIC: 0 },
    "LOADI": { OP: "Annn", OPERANDS: 1, SOURCE: 0, TARGET: 0, NUMERIC: 3 },
    "JUMPI": { OP: "Bnnn", OPERANDS: 1, SOURCE: 0, TARGET: 0, NUMERIC: 3 },
    "RAND" : { OP: "Ctnn", OPERANDS: 2, SOURCE: 0, TARGET: 1, NUMERIC: 2 },
    "DRAW" : { OP: "Dstn", OPERANDS: 3, SOURCE: 1, TARGET: 1, NUMERIC: 1 },
    "MOVED": { OP: "Ft07", OPERANDS: 1, SOURCE: 0, TARGET: 1, NUMERIC: 0 },
    "KEYD" : { OP: "Ft0A", OPERANDS: 1, SOURCE: 0, TARGET: 1, NUMERIC: 0 },
    "LOADD": { OP: "Fs15", OPERANDS: 1, SOURCE: 1, TARGET: 0, NUMERIC: 0 },
    "LOADS": { OP: "Fs18", OPERANDS: 1, SOURCE: 1, TARGET: 0, NUMERIC: 0 },
    "ADDI" : { OP: "Fs1E", OPERANDS: 1, SOURCE: 1, TARGET: 0, NUMERIC: 0 },
    "LDSPR": { OP: "Fs29", OPERANDS: 1, SOURCE: 1, TARGET: 0, NUMERIC: 0 },
    "BCD"  : { OP: "Fs33", OPERANDS: 1, SOURCE: 1, TARGET: 0, NUMERIC: 0 },
    "STOR" : { OP: "Fs55", OPERANDS: 1, SOURCE: 1, TARGET: 0, NUMERIC: 0 },
    "READ" : { OP: "Fs65", OPERANDS: 1, SOURCE: 1, TARGET: 0, NUMERIC: 0 },
}

# Pseudo operations
END = "END"
ORG = "ORG"
EQU = "EQU"
INCLUDE = "INCLUDE"
PSEUDO_OPERATIONS = [ END, ORG, EQU, INCLUDE ]

# Pattern to parse a single line
ASM_LINE_REGEX = re.compile("(?P<" + LABEL + ">\w*)\s+(?P<" + OP + ">\w*)\s+"
    "(?P<" + OPERANDS + ">[\w#\$,\+-]*)\s+(?P<" + COMMENT + ">.*)")

# C L A S S E S ###############################################################

class TranslationError(Exception):
    '''
    Translation errors occur when the translate function is called from 
    within the Statement class. Translation errors usually refer to the fact
    that an invalid mnemonic or invalid register was specified.
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Statement:
    '''
    The Statement class represents a single line of assembly language. Each
    statement is constructed from a single line that has the following format:

        LABEL   MNEMONIC   OPERANDS    COMMENT

    The statement can be parsed and translated to its Chip8 machine code
    equivalent.
    '''
    def __init__(self):
        self.opcode = ""
        self.op = ""
        self.label = ""
        self.operands = ""
        self.comment = ""
        self.size = 0
        self.source = ""
        self.target = ""
        self.numeric = ""

    def __str__(self):
        return "{}  {}  {}  {}".format(self.label, self.op,
               self.operands, self.comment)

    def parse_line(self, line):
        '''
        Parse a line of assembly language text.
        '''
        data = ASM_LINE_REGEX.match(line)
        if data:
            self.label = data.group(LABEL)
            self.op = data.group(OP)
            self.operands = data.group(OPERANDS)
            self.comment = data.group(COMMENT)

    def translate(self):
        '''
        Translate the text into an actual opcode.
        '''
        if self.op in PSEUDO_OPERATIONS:
            self.source = 0
            self.target = 0
            self.numeric = 0
            return 

        if self.op not in OPERATIONS:
            error = "Invalid mnemonic '{}'".format(self.op)
            raise TranslationError(error)

        operation = OPERATIONS[self.op]
        self.opcode = operation[OP]
        operands = self.operands.split(",")

        if len(operands) != operation[OPERANDS]:
            error = "Expected {} operand(s), but got {}".format(
               operation[OPERANDS], len(operands))
            raise TranslationError(error)

        counter = 0
        for operand_type in [SOURCE, TARGET, NUMERIC]:
            if operation[operand_type] != 0:
                self.set_value(operand_type, operands[counter])
                counter += 1


    def set_value(self, operand_type, operand):
        '''
        Given the type of operand we expect, as well as an operand value,
        set the operand to the correct value, checking to make sure that
        the value type matches what we expect.

        @param operand_type: the type of the operand we expect
        @type: [ str ]

        @param operand: the value of the operand we are passing in
        @type: str
        '''
        if operand_type == SOURCE or operand_type == TARGET:
            setattr(self, operand_type, self.get_register(operand))
        else:
            setattr(self, operand_type, self.get_value(operand))

    def is_register(self, string):
        '''
        Checks to see if a register is specified. Registers start with 'r' or
        'R'. All registers are specified in hex - R0 through RF.

        @param string: a string representing the operand
        @type string: str
        '''
        return string.lower().startswith("r")

    def get_value(self, string):
        if string.startswith("$"):
            return hex(int(string[1:], 16))
        return string

    def get_register(self, string):
        if not self.is_register(string):
            error = "Expected register, but got [{}]".format(operand)
            raise TranslationError(error)

        if len(string) > 2:
            error = "Invalid register [{}]".format(operand)

        return hex(int(string[1:],16))
      
    def is_pseudo_op(self):
        '''
        Returns true if the assembly language statement is actually a pseudo op.
    
        @return: True if the statement is a pseudo op, False otherwise
        @rtype: boolean
        '''
        if self.op in PSEUDO_OPERATIONS:
            return True
        return False


    def is_empty(self):
        '''
        Returns True if there is no label that is contained within the 
        statement.

        @return: True if the statement is empty, False otherwise
        @rtype: boolean
        '''
        return self.op == ""


    def get_label(self):
        '''
        Returns the label associated with this statement.

        @return: the label for this statement
        @rtype: str
        '''
        return self.label

# F U N C T I O N S ###########################################################

def parse_arguments():
    '''
    Parses the command-line arguments passed to the assembler.
    '''
    parser = argparse.ArgumentParser(description = "Assemble or disassmble "
        "machine language code for the Chip8. See README.md for more "
        "information, and LICENSE for terms of use.")
    parser.add_argument("filename", help = "the name of the file to examine")
    parser.add_argument("-s", action = "store_true", help = "print out the " 
        "symbol table")
    return parser.parse_args()


def read_file(filename):
    '''
    Returns a list of all of the strings contained within the file called
    filename. Each string in the list represents one line of the file.

    @param filename: the name of the file to open
    @type filename: str

    @return: a list of strings read from the file
    @rtype: [ str ]
    '''
    return open(filename).readlines()


def main(args):
    '''
    Runs the assembler with the specified arguments.

    @param args: the arguments to the main function
    @type: namedtuple
    '''
    symbol_table = dict()
    statements = []

    # Pass 1: parse all of the statements in the file, but do not attempt
    # to resolve any of the labels or locations
    print "Processing [{}]".format(args.filename) 
    print "Pass 1:",
    with open(args.filename) as infile:
        for line in infile:
            statement = Statement()
            statement.parse_line(line)
            if not statement.is_empty():
                statements.append(statement)
    print "{} statement(s) parsed".format(len(statements))

    # Pass 2: translate the statements into their respective opcodes
    print "Pass 2:",
    for index in xrange(len(statements)):
        statement = statements[index]
        try:
            statement.translate()
        except TranslationError as error:
            print "translation error"
            print "Error: " + error.value
            print "Line: " + str(statement)
            sys.exit(1)
        label = statement.get_label()
        if label:
            if label in symbol_table:
                print "symbol error"
                print "Error: label [" + label + "] redefined"
                print "Line: " + str(statement)
                sys.exit(1)
            symbol_table[label] = index
    print "{} operations translated".format(len(statements))

    # Check to see if the user wanted to print the symbol table
    if args.s:
        print("-- Symbol Table --")
        for symbol, value in symbol_table.iteritems():
            print("{} {}".format(symbol, value))
            


# M A I N #####################################################################

if __name__ == "__main__":
    main(parse_arguments())

# E N D   O F   F I L E #######################################################
