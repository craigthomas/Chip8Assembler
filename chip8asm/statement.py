"""
Copyright (C) 2024 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

This file contains Exceptions for the Chip 8 Assembler.
"""
# I M P O R T S ###############################################################

import re

from collections import namedtuple
from copy import copy

from chip8asm.exceptions import TranslationError, ParseError

# C O N S T A N T S ###########################################################

SOURCE = "source"
TARGET = "target"
NUMERIC = "numeric"
SOURCE_REG = "s"
TARGET_REG = "t"
NUMERIC_REG = "n"

Operation = namedtuple('Operation', ['mnemonic', 'op', 'operands', 'source', 'target', 'numeric'])

OPERATIONS = [
    Operation(op="0nnn", operands=1, source=0, target=0, numeric=3, mnemonic="SYS"),
    Operation(op="00E0", operands=0, source=0, target=0, numeric=0, mnemonic="CLR"),
    Operation(op="00EE", operands=0, source=0, target=0, numeric=0, mnemonic="RTS"),
    Operation(op="1nnn", operands=1, source=0, target=0, numeric=3, mnemonic="JUMP"),
    Operation(op="2nnn", operands=1, source=0, target=0, numeric=3, mnemonic="CALL"),
    Operation(op="3snn", operands=2, source=1, target=0, numeric=2, mnemonic="SKE"),
    Operation(op="4snn", operands=2, source=1, target=0, numeric=2, mnemonic="SKNE"),
    Operation(op="5st0", operands=2, source=1, target=1, numeric=0, mnemonic="SKRE"),
    Operation(op="6snn", operands=2, source=1, target=0, numeric=2, mnemonic="LOAD"),
    Operation(op="7snn", operands=2, source=1, target=0, numeric=2, mnemonic="ADD"),
    Operation(op="8st0", operands=2, source=1, target=1, numeric=0, mnemonic="MOVE"),
    Operation(op="8st1", operands=2, source=1, target=1, numeric=0, mnemonic="OR"),
    Operation(op="8st2", operands=2, source=1, target=1, numeric=0, mnemonic="AND"),
    Operation(op="8st3", operands=2, source=1, target=1, numeric=0, mnemonic="XOR"),
    Operation(op="8st4", operands=2, source=1, target=1, numeric=0, mnemonic="ADDR"),
    Operation(op="8st5", operands=2, source=1, target=1, numeric=0, mnemonic="SUB"),
    Operation(op="8st6", operands=1, source=1, target=1, numeric=0, mnemonic="SHR"),
    Operation(op="8st7", operands=2, source=1, target=1, numeric=0, mnemonic="SUBN"),
    Operation(op="8stE", operands=1, source=1, target=1, numeric=0, mnemonic="SHL"),
    Operation(op="9st0", operands=2, source=1, target=1, numeric=0, mnemonic="SKRNE"),
    Operation(op="Annn", operands=1, source=0, target=0, numeric=3, mnemonic="LOADI"),
    Operation(op="Bnnn", operands=1, source=0, target=0, numeric=3, mnemonic="JUMPI"),
    Operation(op="Ctnn", operands=2, source=0, target=1, numeric=2, mnemonic="RAND"),
    Operation(op="Dstn", operands=3, source=1, target=1, numeric=1, mnemonic="DRAW"),
    Operation(op="Es9E", operands=1, source=1, target=0, numeric=0, mnemonic="SKPR"),
    Operation(op="EsA1", operands=1, source=1, target=0, numeric=0, mnemonic="SKUP"),
    Operation(op="Ft07", operands=1, source=0, target=1, numeric=0, mnemonic="MOVED"),
    Operation(op="Ft0A", operands=1, source=0, target=1, numeric=0, mnemonic="KEYD"),
    Operation(op="Fs15", operands=1, source=1, target=0, numeric=0, mnemonic="LOADD"),
    Operation(op="Fs18", operands=1, source=1, target=0, numeric=0, mnemonic="LOADS"),
    Operation(op="Fs1E", operands=1, source=1, target=0, numeric=0, mnemonic="ADDI"),
    Operation(op="Fs29", operands=1, source=1, target=0, numeric=0, mnemonic="LDSPR"),
    Operation(op="Fs33", operands=1, source=1, target=0, numeric=0, mnemonic="BCD"),
    Operation(op="Fs55", operands=1, source=1, target=0, numeric=0, mnemonic="STOR"),
    Operation(op="Fs65", operands=1, source=1, target=0, numeric=0, mnemonic="READ"),
    # Super Chip 8 Instructions
    Operation(op="00Cn", operands=1, source=0, target=0, numeric=1, mnemonic="SCRD"),
    Operation(op="00FB", operands=0, source=0, target=0, numeric=0, mnemonic="SCRR"),
    Operation(op="00FC", operands=0, source=0, target=0, numeric=0, mnemonic="SCRL"),
    Operation(op="00FD", operands=0, source=0, target=0, numeric=0, mnemonic="EXIT"),
    Operation(op="00FE", operands=0, source=0, target=0, numeric=0, mnemonic="EXTD"),
    Operation(op="00FF", operands=0, source=0, target=0, numeric=0, mnemonic="EXTE"),
    Operation(op="Fs75", operands=1, source=1, target=0, numeric=0, mnemonic="SRPL"),
    Operation(op="Fs85", operands=1, source=1, target=0, numeric=0, mnemonic="LRPL"),
    # XO Chip Instructions
    Operation(op="5st2", operands=2, source=1, target=1, numeric=0, mnemonic="SAVESUB"),
    Operation(op="F002", operands=0, source=0, target=0, numeric=0, mnemonic="AUDIO"),
    Operation(op="Fn03", operands=1, source=0, target=0, numeric=1, mnemonic="PLANE"),
    Operation(op="Fs3A", operands=1, source=1, target=0, numeric=0, mnemonic="PITCH"),
]

# Pseudo operations
FCB = "FCB"
FDB = "FDB"
PSEUDO_OPERATIONS = [FCB, FDB]

# Pattern to recognize a blank line
BLANK_LINE_REGEX = re.compile(r"^\s*$")

# Pattern to parse a comment line
COMMENT_LINE_REGEX = re.compile(r"^\s*#\s*(?P<comment>.*)$")

# Pattern to parse a single line
ASM_LINE_REGEX = re.compile(
    r"^(?P<label>\w*)\s+(?P<mnemonic>\w*)\s+(?P<operands>[\w$,+-]*)\s*[#]*\s*(?P<comment>.*)$"
)

# Pattern to match a register
REG_LINE_REGEX = re.compile("[rR][0-9a-fA-F]$")

# C L A S S E S ###############################################################


class Statement(object):
    """
    The Statement class represents a single line of assembly language. Each
    statement is constructed from a single line that has the following format:

        LABEL   MNEMONIC   OPERANDS    COMMENT

    The statement can be parsed and translated to its Chip8 machine code
    equivalent.
    """
    def __init__(self):
        self.empty = True
        self.comment_only = False
        self.operation = None
        self.label = None
        self.operands = None
        self.comment = None
        self.size = 0
        self.address = None
        self.mnemonic = None
        self.op_code = None
        self.source = None
        self.target = None
        self.numeric = None

    def __str__(self):
        return "0x{} {} {} {} {}  # {}".format(
            self.get_address()[2:].upper().rjust(4, '0'),
            self.get_op_code().upper().rjust(4, '0'),
            self.get_label().rjust(10, ' '),
            self.get_mnemonic().rjust(5, ' '),
            self.get_operands().rjust(15, ' '),
            self.get_comment().ljust(40, ' ')
        )

    @staticmethod
    def is_register(string):
        """
        Checks to see if a register is specified. Registers start with 'r' or
        'R'. All registers are specified in hex - R0 through RF.

        :param string: a string representing the operand
        :return: True if the string is a register, False otherwise
        """
        return REG_LINE_REGEX.match(string) is not None

    @staticmethod
    def get_value(string):
        """
        Return the hex representation of the value if it starts with a '$'.
        Otherwise, just return the value itself, since it is likely a label.

        :param string: the string to scan
        :return: the hex representation of the value, or the label
        """
        return hex(int(string[1:], 16))[2:].upper() if string.startswith("$") else string

    @staticmethod
    def get_register(string):
        """
        Returns the register number specified.

        :param string: the hex representation of the register number
        """
        if not Statement.is_register(string):
            raise TranslationError("expected register in r0-rF, but got [{}]".format(string))
        if len(string) > 2:
            raise TranslationError("invalid register [{}]".format(string))
        return hex(int(string[1:], 16))[-1].upper()

    def is_pseudo_op(self):
        """
        Returns true if the assembly language statement is actually a pseudo op.

        :return: True if the statement is a pseudo op, False otherwise
        """
        return self.mnemonic in PSEUDO_OPERATIONS

    def has_comment(self):
        """
        Returns True if there is a comment for the statement.

        :return: True if there is a comment, False otherwise
        """
        return self.comment is not None

    def is_empty(self):
        """
        Returns True if there is no operation that is contained within the
        statement.

        :return: True if the statement is empty, False otherwise
        """
        return self.empty

    def get_label(self):
        """
        Returns the label associated with this statement.

        :return: the label for this statement
        """
        return self.label or ""

    def get_comment(self):
        """
        Returns the comment for this statement.

        :return: the comment for this statement
        """
        return self.comment or ""

    def get_address(self):
        """
        Returns the address for this statement.

        :return: the address for this statement
        """
        return self.address or ""

    def set_address(self, address):
        """
        Set the address of the current operation in hex.

        :param address: the address of the operation
        """
        self.address = address

    def get_mnemonic(self):
        """
        Returns the mnemonic for this statement.

        :return: the mnemonic for this statement
        """
        return self.mnemonic or ""

    def get_op_code(self):
        """
        Returns the operation code for this statement.

        :return: the operation code for this statement
        """
        return self.op_code or ""

    def get_operands(self):
        """
        Returns the operands for this statement.

        :return: the operands for this statement
        """
        return self.operands or ""

    def parse_line(self, line):
        """
        Parse a line of assembly language text.
        """
        if BLANK_LINE_REGEX.search(line):
            return

        data = COMMENT_LINE_REGEX.match(line)
        if data:
            self.empty = False
            self.comment_only = True
            self.comment = data.group("comment").strip()
            return

        data = ASM_LINE_REGEX.match(line)
        if data:
            self.label = data.group("label") or None
            self.mnemonic = data.group("mnemonic") or None
            self.operands = data.group("operands") or None
            self.comment = data.group("comment").strip() or None
            self.empty = False
            return

        raise ParseError("could not parse line [{}]".format(line))

    def translate(self):
        """
        Translate the mnemonic into an actual operation.
        """
        if self.comment_only:
            return

        if self.is_pseudo_op():
            if not self.operands:
                raise TranslationError(
                    "pseudo operation [{}] requires 1 operand".format(
                        self.mnemonic
                    )
                )
            return

        for operation in OPERATIONS:
            if operation.mnemonic == self.mnemonic:
                self.operation = copy(operation)
                break

        if not self.operation:
            raise TranslationError("invalid mnemonic [{}]'".format(self.mnemonic))

        operands = self.operands.split(",") if self.operands else []
        num_operands = len(operands)
        if num_operands != self.operation.operands:
            raise TranslationError(
                "expected {} operand(s), but got {}".format(
                    self.operation.operands, num_operands
                )
            )

        operand_counter = 0
        if self.operation.source != 0:
            self.source = self.get_register(operands[operand_counter])
            operand_counter += 1

        if self.operation.target != 0:
            self.target = self.get_register(operands[operand_counter])
            operand_counter += 1

        if self.operation.numeric != 0:
            self.numeric = self.get_value(operands[operand_counter])

    def replace_label(self, label, value):
        """
        Given a label and a value, replace the source, target, or numeric
        values with the given value if they are a label.

        :param label: the label to replace
        :param value: the value to replace the label with
        """
        self.source = value if self.source == label else self.source
        self.target = value if self.target == label else self.target
        self.numeric = value if self.numeric == label else self.numeric

    def fix_values(self):
        """
        Translate the source, target, and numeric values into the appropriate
        parts of the op code. For pseudo operations, simply copy the value to
        the op code.
        """
        if self.comment_only:
            return

        if self.is_pseudo_op():
            if not self.operands.startswith("$"):
                raise TranslationError(
                    "expected value starting with $, but got {}".format(
                        self.operands
                    )
                )
            self.op_code = self.get_value(self.operands)
            return

        self.op_code = self.operation.op
        if self.operation.source == 1:
            if len(self.source) > 1:
                raise TranslationError(
                    "expected source in 0-F, but got {}".format(self.source)
                )
            self.op_code = self.op_code.replace(SOURCE_REG, self.source)
        if self.operation.target == 1:
            if len(self.target) > 1:
                raise TranslationError(
                    "expected target in 0-F, but got {}".format(self.target)
                )
            self.op_code = self.op_code.replace(TARGET_REG, self.target)
        if self.operation.numeric != 0:
            if len(self.numeric) > self.operation.numeric:
                raise TranslationError("expected numeric of length {}, but was length {} [{}]".format(
                    self.operation.numeric, len(self.numeric), self.numeric)
                )
            numeric = self.numeric.zfill(self.operation.numeric)
            numeric_string = NUMERIC_REG * self.operation.numeric
            self.op_code = self.op_code.replace(numeric_string, numeric)


# E N D   O F   F I L E #######################################################
