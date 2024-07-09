"""
Copyright (C) 204 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

A Chip 8 assembler - see the README.md file for details.
"""
# I M P O R T S ###############################################################

import unittest

from chip8asm.program import Program
from chip8asm.statement import Statement

# C L A S S E S ###############################################################


class TestIntegration(unittest.TestCase):
    """
    A test class for integration tests.
    """
    def setUp(self):
        """
        Common setup routines needed for all unit tests.
        """
        pass

    @staticmethod
    def translate_statements(program):
        """
        Given a program, translate the statements into machine code.
        """
        program.translate_statements()
        program.set_addresses()
        program.fix_opcodes()
        return program

    def test_audio_mnemonic_translate_correct(self):
        program = Program()
        statement = Statement()
        statement.parse_line("    AUDIO    ; audio statement")
        program.statements.append(statement)
        program = self.translate_statements(program)
        machine_code = program.generate_machine_code()
        self.assertEqual([0xF0, 0x02], machine_code)

    def test_pitch_mnemonic_translate_correct(self):
        program = Program()
        statement = Statement()
        statement.parse_line("    PITCH r1    ; pitch statement")
        program.statements.append(statement)
        program = self.translate_statements(program)
        machine_code = program.generate_machine_code()
        self.assertEqual([0xF1, 0x3A], machine_code)

    def test_plane_mnemonic_translate_correct(self):
        program = Program()
        statement = Statement()
        statement.parse_line("    PLANE $2    ; plane statement")
        program.statements.append(statement)
        program = self.translate_statements(program)
        machine_code = program.generate_machine_code()
        self.assertEqual([0xF2, 0x03], machine_code)

    def test_savesub_mnemonic_translate_correct(self):
        program = Program()
        statement = Statement()
        statement.parse_line("    SAVESUB r1,r6    ; save subset statement")
        program.statements.append(statement)
        program = self.translate_statements(program)
        machine_code = program.generate_machine_code()
        self.assertEqual([0x51, 0x62], machine_code)

    def test_loadsub_mnemonic_translate_correct(self):
        program = Program()
        statement = Statement()
        statement.parse_line("    LOADSUB r1,r6    ; load subset statement")
        program.statements.append(statement)
        program = self.translate_statements(program)
        machine_code = program.generate_machine_code()
        self.assertEqual([0x51, 0x63], machine_code)

    def test_scrollup_mnemonic_translate_correct(self):
        program = Program()
        statement = Statement()
        statement.parse_line("    SCRU 5    ; scroll up statement")
        program.statements.append(statement)
        program = self.translate_statements(program)
        machine_code = program.generate_machine_code()
        self.assertEqual([0x00, 0xD5], machine_code)

# E N D   O F   F I L E #######################################################
