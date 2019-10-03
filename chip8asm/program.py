"""
Copyright (C) 2014-2019 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

This file contains the main Program class for the Chip 8 Assembler.
"""
# I M P O R T S ###############################################################

import sys

from chip8asm.exceptions import TranslationError
from chip8asm.statement import Statement, FCB

# C L A S S E S ###############################################################


class Program(object):
    """
    The Program class represents an actual Chip 8 program. Each Program
    contains a list of statements. Additionally, a Program keeps track of all
    the user-defined symbols in the program.
    """
    def __init__(self):
        self.symbol_table = dict()
        self.statements = []
        self.address = 0x200

    def parse_file(self, filename):
        """
        Parses all of the lines in a file, and transforms each one into
        a Statement.

        :param filename: the name of the file to parse
        """
        with open(filename) as infile:
            for line in infile:
                statement = Statement()
                statement.parse_line(line)
                if not statement.is_empty():
                    self.statements.append(statement)

    def translate_statements(self):
        """
        Translates all the parsed statements into their respective
        opcodes.
        """
        for index, statement in enumerate(self.statements):
            try:
                statement.translate()
            except TranslationError as error:
                self.throw_error(error, statement)
            label = statement.get_label()
            if label:
                if label in self.symbol_table:
                    error = TranslationError("label [" + label + "] redefined")
                    self.throw_error(error, statement)
                self.symbol_table[label] = index

    def set_addresses(self):
        """
        Determines the address that each label refers to.
        """
        for statement in self.statements:
            label = statement.get_label()
            if label:
                self.symbol_table[label] = hex(self.address)
            statement.set_address(hex(self.address))
            if not statement.comment_only and not statement.is_empty():
                self.address += 1 if statement.operation == FCB else 2

    def fix_opcodes(self):
        """
        Calculates the final opcode for each statement in the program.
        """
        for statement in self.statements:
            for label, value in self.symbol_table.items():
                statement.replace_label(label, value[2:])
            try:
                statement.fix_values()
            except TranslationError as error:
                self.throw_error(error, statement)

    def get_symbol_table(self):
        """
        Returns the symbol table dictionary for the parsed program.

        :return: the symbol table for the program
        """
        return self.symbol_table

    def get_statements(self):
        """
        Returns the statements that make up the program.

        :return: the statements for the program
        """
        return self.statements

    def save_binary_file(self, filename):
        """
        Writes out the assembled statements to the specified file
        name.

        :param filename: the name of the file to save statements
        """
        machine_codes = []
        for statement in self.statements:
            if not statement.is_empty() and not statement.comment_only:
                for index in range(0, len(statement.op_code), 2):
                    machine_codes.append(int(statement.op_code[index:index + 2], 16))
        with open(filename, "wb") as outfile:
            outfile.write(bytearray(machine_codes))

    @staticmethod
    def throw_error(error, statement):
        """
        Prints out an error message.

        :param error: the error message to throw
        :param statement: the assembly statement that caused the error
        """
        print(error.value)
        print("line: {}".format(str(statement)))
        sys.exit(1)

# E N D   O F   F I L E #######################################################
