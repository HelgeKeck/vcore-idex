# /usr/bin/python3

import sys
import re
import argparse
from shutil import ReadError, copy2
from os import path, remove, getenv

def argumentparser():
    """
        ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog=path.basename(__file__),
        description='** IDEX Post Processing Script ** \n\r',
        epilog='Result: Adds a variable to the start gcode that tells if both toolheads are used or not.')

    parser.add_argument('input_file', metavar='gcode-files', type=str, nargs='+',
                        help='One or more GCode file(s) to be processed '
                        '- at least one is required.')

    try:
        args = parser.parse_args()
        return args

    except IOError as msg:
        parser.error(str(msg))


def main(args):
    """
        MAIN
    """
    print(args.input_file)

    for sourcefile in args.input_file:
        if path.exists(sourcefile):
            process_gcodefile(args, sourcefile)


def process_gcodefile(args, sourcefile):
    """
        MAIN Processing.
        To do with ever file from command line.
    """

    # Read the ENTIRE GCode file into memory
    try:
        with open(sourcefile, "r", encoding='UTF-8') as readfile:
            lines = readfile.readlines()
    except ReadError as exc:
        print('FileReadError:' + str(exc))
        sys.exit(1)

    t_count = 0
    writefile = None

    try:
        with open(sourcefile, "w", newline='\n', encoding='UTF-8') as writefile:
            # search for toolhead changes
            for i, strline in enumerate(lines):
                if strline.startswith(";tool change post processor tag"):
                    t_count += 1
                if t_count == 2:
                    break
            # add result to start print macro
            for i, strline in enumerate(lines):
                if strline.startswith("START_PRINT"):
                    if t_count == 2:
                        strline = strline.rstrip() + ' BOTH_TOOLHEADS=True\n'
                    else:
                        strline = strline.rstrip() + ' BOTH_TOOLHEADS=False\n'
                writefile.write(strline)
    except Exception as exc:
        print("Oops! Something went wrong. " + str(exc))
        sys.exit(1)
    finally:
        writefile.close()
        readfile.close()

ARGS = argumentparser()

main(ARGS)
