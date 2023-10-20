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

    # test for multiple toolchanges
    tag_count = 0
    start_print_line = 0
    for line in range(len(lines)):
        if lines[line].rstrip().startswith("START_PRINT") and start_print_line == 0:
            start_print_line = line
        if lines[line].rstrip().startswith(";tool change post processor tag"):
            tag_count += 1
        if tag_count == 2:
            break
    if tag_count < 2:
        lines[start_print_line] = lines[start_print_line].rstrip() + ' BOTH_TOOLHEADS=False\n'

    # get min max x 
    min_x = 1000
    max_x = 0
    if start_print_line > 0:
        for line in range(len(lines)):
            if lines[line].rstrip().startswith("G1") or lines[line].rstrip().startswith("G0"):
                split = lines[line].rstrip().replace("  ", " ").split(" ")
                for s in range(len(split)):
                    if split[s].lower().startswith("x"):
                        try:
                            x = float(split[1].lower().replace("x", ""))
                            if x < min_x:
                                min_x = x
                            if x > max_x:
                                max_x = x
                        except Exception as exc:
                            print("Oops! Something went wrong. " + str(exc))
                            print("line:" + lines[line].rstrip())
                            sys.exit(1)
        if min_x < 1000:
            lines[start_print_line] = lines[start_print_line].rstrip() + ' MIN_X=' + str(min_x) + ' MAX_X=' + str(max_x)

    # write file if changed
    if tag_count < 2:
        writefile = None
        try:
            with open(sourcefile, "w", newline='\n', encoding='UTF-8') as writefile:
                for i, strline in enumerate(lines):
                    writefile.write(strline)
        except Exception as exc:
            print("Oops! Something went wrong. " + str(exc))
            sys.exit(1)
        finally:
            writefile.close()
            readfile.close()

ARGS = argumentparser()

main(ARGS)
