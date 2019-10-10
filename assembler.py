"""
Copyright (C) 2014-2018 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

A Chip 8 assembler - see the README.md file for details.
"""
# I M P O R T S ###############################################################

import argparse

from chip8asm.program import Program

# F U N C T I O N S ###########################################################


def parse_arguments():
    """
    Parses the command-line arguments passed to the assembler.
    """
    parser = argparse.ArgumentParser(
        description="Assemble or disassemble "
        "machine language code for the Chip8. See README.md for more "
        "information, and LICENSE for terms of use."
    )
    parser.add_argument("filename", help="the name of the file to examine")
    parser.add_argument(
        "--symbols", action="store_true", help="print out the symbol table"
    )
    parser.add_argument(
        "--print", action="store_true",
        help="print out the assembled statements when finished"
    )
    parser.add_argument(
        "--output", metavar="FILE", help="stores the assembled program in FILE")
    return parser.parse_args()


def main(args):
    """
    Runs the assembler with the specified arguments.

    @param args: the arguments to the main function
    @type: namedtuple
    """
    program = Program()
    program.parse_file(args.filename)
    program.translate_statements()
    program.set_addresses()
    program.fix_opcodes()

    if args.symbols:
        print("-- Symbol Table --")
        for symbol, value in program.get_symbol_table().items():
            print("0x{} {}".format(value[2:].rjust(4, '0').upper(), symbol))

    if args.print:
        print("-- Assembled Statements --")
        for statement in program.get_statements():
            print(statement)

    if args.output:
        program.save_binary_file(args.output)


main(parse_arguments())

# E N D   O F   F I L E #######################################################
