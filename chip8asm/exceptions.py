"""
Copyright (C) 2014-2019 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

This file contains Exceptions for the Chip 8 Assembler.
"""
# C L A S S E S ###############################################################


class TranslationError(Exception):
    """
    Translation errors occur when the translate function is called from
    within the Statement class. Translation errors usually refer to the fact
    that an invalid mnemonic or invalid register was specified.
    """
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)


class ParseError(Exception):
    """
    Parse errors occur when the parse function is called from
    within the Statement class. Parse errors usually refer to the fact
    that an invalid line of assembly code was encountered.
    """
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)

# E N D   O F   F I L E #######################################################
