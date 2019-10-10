"""
Copyright (C) 2012-2019 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

A Chip 8 assembler - see the README.md file for details.
"""
# I M P O R T S ###############################################################

import unittest

from chip8asm.exceptions import TranslationError, ParseError

# C L A S S E S ###############################################################


class TestTranslationError(unittest.TestCase):
    """
    A test class for the Chip 8 TranslationError class.
    """
    def setUp(self):
        """
        Common setup routines needed for all unit tests.
        """
        pass

    def test_string_representation(self):
        translation_error = TranslationError("translation error")
        self.assertEqual("'translation error'", str(translation_error))


class TestParseError(unittest.TestCase):
    """
    A test class for the Chip 8 ParseError class.
    """
    def setUp(self):
        """
        Common setup routines needed for all unit tests.
        """
        pass

    def test_string_representation(self):
        parse_error = ParseError("parse error")
        self.assertEqual("'parse error'", str(parse_error))

# E N D   O F   F I L E #######################################################
