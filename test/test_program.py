"""
Copyright (C) 2012-2019 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

A Chip 8 assembler - see the README.md file for details.
"""
# I M P O R T S ###############################################################

import unittest

from chip8asm.program import Program
from chip8asm.statement import Statement

# C L A S S E S ###############################################################


class TestProgram(unittest.TestCase):
    """
    A test class for the Chip 8 Program class.
    """
    def setUp(self):
        """
        Common setup routines needed for all unit tests.
        """
        pass

    def test_get_symbol_table_correct(self):
        program = Program()
        self.assertEqual(dict(), program.get_symbol_table())
        program.symbol_table = dict(test="blah")
        self.assertEqual(dict(test="blah"), program.get_symbol_table())

    def test_get_statements_correct(self):
        program = Program()
        statement = Statement()

        self.assertEqual([], program.get_statements())
        program.statements.append(statement)
        self.assertEqual([statement], program.get_statements())


# E N D   O F   F I L E #######################################################
