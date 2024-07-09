"""
Copyright (C) 2024 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

A Chip 8 assembler - see the README.md file for details.
"""
# I M P O R T S ###############################################################

import unittest

from chip8asm.statement import Statement, OPERATIONS
from chip8asm.exceptions import ParseError, TranslationError

# C L A S S E S ###############################################################


class TestStatement(unittest.TestCase):
    """
    A test class for the Chip 8 Statement class.
    """
    def setUp(self):
        """
        Common setup routines needed for all unit tests.
        """
        pass

    def test_is_register_recognizes_only_registers(self):
        self.assertTrue(Statement.is_register("r0"))
        self.assertTrue(Statement.is_register("r1"))
        self.assertTrue(Statement.is_register("r2"))
        self.assertTrue(Statement.is_register("r3"))
        self.assertTrue(Statement.is_register("r4"))
        self.assertTrue(Statement.is_register("r5"))
        self.assertTrue(Statement.is_register("r6"))
        self.assertTrue(Statement.is_register("r7"))
        self.assertTrue(Statement.is_register("r8"))
        self.assertTrue(Statement.is_register("r9"))
        self.assertTrue(Statement.is_register("ra"))
        self.assertTrue(Statement.is_register("rb"))
        self.assertTrue(Statement.is_register("rc"))
        self.assertTrue(Statement.is_register("rd"))
        self.assertTrue(Statement.is_register("re"))
        self.assertTrue(Statement.is_register("rf"))

        self.assertTrue(Statement.is_register("rA"))
        self.assertTrue(Statement.is_register("rB"))
        self.assertTrue(Statement.is_register("rC"))
        self.assertTrue(Statement.is_register("rD"))
        self.assertTrue(Statement.is_register("rE"))
        self.assertTrue(Statement.is_register("rF"))

        self.assertTrue(Statement.is_register("R0"))
        self.assertTrue(Statement.is_register("R1"))
        self.assertTrue(Statement.is_register("R2"))
        self.assertTrue(Statement.is_register("R3"))
        self.assertTrue(Statement.is_register("R4"))
        self.assertTrue(Statement.is_register("R5"))
        self.assertTrue(Statement.is_register("R6"))
        self.assertTrue(Statement.is_register("R7"))
        self.assertTrue(Statement.is_register("R8"))
        self.assertTrue(Statement.is_register("R9"))
        self.assertTrue(Statement.is_register("Ra"))
        self.assertTrue(Statement.is_register("Rb"))
        self.assertTrue(Statement.is_register("Rc"))
        self.assertTrue(Statement.is_register("Rd"))
        self.assertTrue(Statement.is_register("Re"))
        self.assertTrue(Statement.is_register("Rf"))

        self.assertTrue(Statement.is_register("RA"))
        self.assertTrue(Statement.is_register("RB"))
        self.assertTrue(Statement.is_register("RC"))
        self.assertTrue(Statement.is_register("RD"))
        self.assertTrue(Statement.is_register("RE"))
        self.assertTrue(Statement.is_register("RF"))

    def test_is_register_rejects_bad_register_names(self):
        self.assertFalse(Statement.is_register("R11"))
        self.assertFalse(Statement.is_register("r11"))
        self.assertFalse(Statement.is_register("R"))
        self.assertFalse(Statement.is_register("r"))
        self.assertFalse(Statement.is_register("register"))

    def test_get_value_returns_hex(self):
        self.assertEqual('10', Statement.get_value("$10"))

    def test_get_register_correct(self):
        self.assertEqual('0', Statement.get_register("r0"))
        self.assertEqual('1', Statement.get_register("r1"))
        self.assertEqual('2', Statement.get_register("r2"))
        self.assertEqual('3', Statement.get_register("r3"))
        self.assertEqual('4', Statement.get_register("r4"))
        self.assertEqual('5', Statement.get_register("r5"))
        self.assertEqual('6', Statement.get_register("r6"))
        self.assertEqual('7', Statement.get_register("r7"))
        self.assertEqual('8', Statement.get_register("r8"))
        self.assertEqual('9', Statement.get_register("r9"))
        self.assertEqual('A', Statement.get_register("rA"))
        self.assertEqual('B', Statement.get_register("rB"))
        self.assertEqual('C', Statement.get_register("rC"))
        self.assertEqual('D', Statement.get_register("rD"))
        self.assertEqual('E', Statement.get_register("rE"))
        self.assertEqual('F', Statement.get_register("rF"))
        self.assertEqual('0', Statement.get_register("R0"))
        self.assertEqual('1', Statement.get_register("R1"))
        self.assertEqual('2', Statement.get_register("R2"))
        self.assertEqual('3', Statement.get_register("R3"))
        self.assertEqual('4', Statement.get_register("R4"))
        self.assertEqual('5', Statement.get_register("R5"))
        self.assertEqual('6', Statement.get_register("R6"))
        self.assertEqual('7', Statement.get_register("R7"))
        self.assertEqual('8', Statement.get_register("R8"))
        self.assertEqual('9', Statement.get_register("R9"))
        self.assertEqual('A', Statement.get_register("RA"))
        self.assertEqual('B', Statement.get_register("RB"))
        self.assertEqual('C', Statement.get_register("RC"))
        self.assertEqual('D', Statement.get_register("RD"))
        self.assertEqual('E', Statement.get_register("RE"))
        self.assertEqual('F', Statement.get_register("RF"))

    def test_get_register_bad_register(self):
        with self.assertRaises(TranslationError):
            Statement.get_register("r11")

    def test_is_pseudo_op_correct(self):
        statement = Statement()
        statement.mnemonic = "FDB"
        self.assertTrue(statement.is_pseudo_op())
        statement.mnemonic = "FCB"
        self.assertTrue(statement.is_pseudo_op())
        statement.mnemonic = "BLAH"
        self.assertFalse(statement.is_pseudo_op())

    def test_has_comment_correct(self):
        statement = Statement()
        self.assertFalse(statement.has_comment())
        statement.comment = "blah"
        self.assertTrue(statement.has_comment())

    def test_is_empty_correct(self):
        statement = Statement()
        self.assertTrue(statement.is_empty())
        statement.empty = False
        self.assertFalse(statement.is_empty())

    def test_get_label_correct(self):
        statement = Statement()
        self.assertEqual("", statement.get_label())
        statement.label = "label"
        self.assertEqual("label", statement.get_label())

    def test_get_comment_correct(self):
        statement = Statement()
        self.assertEqual("", statement.get_comment())
        statement.comment = "comment"
        self.assertEqual("comment", statement.get_comment())

    def test_get_mnemonic_correct(self):
        statement = Statement()
        self.assertEqual("", statement.get_mnemonic())
        statement.mnemonic = "mnemonic"
        self.assertEqual("mnemonic", statement.get_mnemonic())

    def test_get_op_code_correct(self):
        statement = Statement()
        self.assertEqual("", statement.get_op_code())
        statement.op_code = "op_code"
        self.assertEqual("op_code", statement.get_op_code())

    def test_get_operands_correct(self):
        statement = Statement()
        self.assertEqual("", statement.get_operands())
        statement.operands = "operands"
        self.assertEqual("operands", statement.get_operands())

    def test_get_address_correct(self):
        statement = Statement()
        self.assertEqual("", statement.get_address())
        statement.address = "address"
        self.assertEqual("address", statement.get_address())

    def test_set_address_correct(self):
        statement = Statement()
        self.assertEqual("", statement.get_address())
        statement.set_address("address")
        self.assertEqual("address", statement.get_address())

    def test_parsing_recognizes_blank_line(self):
        statement = Statement()
        statement.parse_line("    ")
        self.assertFalse(statement.has_comment())
        self.assertIsNone(statement.comment)
        self.assertIsNone(statement.operation)
        self.assertIsNone(statement.label)
        self.assertIsNone(statement.operands)
        self.assertIsNone(statement.address)
        self.assertIsNone(statement.mnemonic)
        self.assertEqual(0, statement.size)

    def test_parsing_recognizes_comment_line(self):
        statement = Statement()
        statement.parse_line("# This is a comment")
        self.assertTrue(statement.has_comment())
        self.assertEqual("This is a comment", statement.comment)
        self.assertIsNone(statement.operation)
        self.assertIsNone(statement.label)
        self.assertIsNone(statement.operands)
        self.assertIsNone(statement.address)
        self.assertIsNone(statement.mnemonic)
        self.assertEqual(0, statement.size)

    def test_parsing_correct_asm_line(self):
        statement = Statement()
        statement.parse_line("label mnemonic operands # comment")
        self.assertTrue(statement.has_comment())
        self.assertEqual("comment", statement.comment)
        self.assertIsNone(statement.operation)
        self.assertEqual("label", statement.label)
        self.assertEqual("operands", statement.operands)
        self.assertIsNone(statement.address)
        self.assertEqual("mnemonic", statement.mnemonic)
        self.assertEqual(0, statement.size)

    def test_parse_bad_line_raises_error(self):
        statement = Statement()
        with self.assertRaises(ParseError):
            statement.parse_line("bad")

    def test_translate_pseudo_op_does_nothing(self):
        statement = Statement()
        statement.parse_line("    FDB $FFEE")
        statement.translate()
        self.assertFalse(statement.has_comment())
        self.assertIsNone(statement.comment)
        self.assertIsNone(statement.operation)
        self.assertIsNone(statement.label)
        self.assertEqual("FDB", statement.mnemonic)
        self.assertEqual("$FFEE", statement.operands)
        self.assertIsNone(statement.address)
        self.assertEqual(0, statement.size)

    def test_translate_pseudo_bad_num_operands_raises_error(self):
        statement = Statement()
        statement.parse_line("    FDB")
        with self.assertRaises(TranslationError):
            statement.translate()

    def test_translate_valid_line_correct(self):
        statement = Statement()
        statement.parse_line("label SKRNE r1,r2 # comment")
        statement.translate()
        self.assertTrue(statement.has_comment())
        self.assertEqual("comment", statement.comment)
        self.assertEqual(OPERATIONS[19], statement.operation)
        self.assertEqual("label", statement.label)
        self.assertEqual("SKRNE", statement.mnemonic)
        self.assertEqual("r1,r2", statement.operands)
        self.assertIsNone(statement.address)
        self.assertEqual(0, statement.size)

    def test_translate_bad_mnemonic_raises_error(self):
        statement = Statement()
        statement.parse_line("label BLAH r1,r2 # comment")
        with self.assertRaises(TranslationError):
            statement.translate()

    def test_translate_bad_num_operands_raises_error(self):
        statement = Statement()
        statement.parse_line("label JUMP  # comment")
        with self.assertRaises(TranslationError):
            statement.translate()

    def test_replace_label_correct(self):
        statement = Statement()
        statement.source = "source"
        statement.target = "target"
        statement.numeric = "numeric"
        statement.replace_label("source", "replaced source")
        self.assertEqual("replaced source", statement.source)
        self.assertEqual("target", statement.target)
        self.assertEqual("numeric", statement.numeric)
        statement.replace_label("target", "replaced target")
        self.assertEqual("replaced source", statement.source)
        self.assertEqual("replaced target", statement.target)
        self.assertEqual("numeric", statement.numeric)
        statement.replace_label("numeric", "replaced numeric")
        self.assertEqual("replaced source", statement.source)
        self.assertEqual("replaced target", statement.target)
        self.assertEqual("replaced numeric", statement.numeric)

# E N D   O F   F I L E #######################################################
