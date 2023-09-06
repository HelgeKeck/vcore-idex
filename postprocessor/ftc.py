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

    writefile = None

    try:
        with open(sourcefile, "w", newline='\n', encoding='UTF-8') as writefile:
 
            # parse gcode
            for line in range(len(lines)):
                if lines[line].rstrip().startswith("; custom gcode: end_filament_gcode"):

                    # z-hop before toolchange
                    zhop = 0
                    zhop_line = 0
                    if lines[line-1].rstrip().startswith("G1 Z"):
                        split = lines[line-1].rstrip().split(" ")
                        if split[1].startswith("Z"):
                            zhop = float(split[1].replace("Z", ""))
                            if zhop > 0.0:
                                zhop_line = line-1

                    # toolchange
                    toolchange_line = 0
                    for i2 in range(20):
                        if lines[line+i2].rstrip().startswith("T0 P1") or lines[line+i2].rstrip().startswith("T1 P1"):
                            toolchange_line = line+i2
                            break

                    # retraction after toolchange
                    retraction_line = 0
                    if toolchange_line > 0:
                        for i2 in range(20):
                            if lines[toolchange_line + i2].rstrip().startswith("G1 E-"):
                                retraction_line = toolchange_line + i2
                                break

                    # move after toolchange
                    move_x = ''
                    move_y = ''
                    move_line = 0
                    if toolchange_line > 0:
                        for i2 in range(20):
                            if lines[toolchange_line + i2].rstrip().replace("  ", " ").startswith("G1 X"):
                                splittedstring = lines[toolchange_line + i2].rstrip().replace("  ", " ").split(" ")
                                if splittedstring[1].startswith("X"):
                                    if splittedstring[2].startswith("Y"):
                                        move_x = splittedstring[1].rstrip()
                                        move_y = splittedstring[2].rstrip()
                                        move_line = toolchange_line + i2
                                        break

                    # z-drop after toolchange
                    zdrop = 0
                    zdrop_line = 0
                    if zhop_line > 0:
                        if lines[move_line + 1].rstrip().startswith("G1 Z"):
                            split = lines[move_line + 1].rstrip().split(" ")
                            if split[1].startswith("Z"):
                                zdrop = float(split[1].replace("Z", ""))
                                if zdrop > 0.0:
                                    zdrop_line = move_line + 1

                    # extrusion after move
                    extrusion_line = 0
                    if move_line > 0:
                        for i2 in range(5):
                            if lines[move_line + i2].rstrip().startswith("G1 E"):
                                extrusion_line = move_line + i2
                                break

                    # make changes
                    if toolchange_line > 0 and move_line > 0:
                        
                        zlift = 0.0
                        if zhop_line > 0 and zdrop_line > 0 and zdrop_line > move_line and zhop > zdrop:
                            zlift = round(zhop - zdrop, 3)
                            if zlift > 0 and zlift < 2:
                                print("Z-Hop removed            " + lines[zhop_line].rstrip())
                                lines[zhop_line] = '; Removed by FTC ' + lines[zhop_line].rstrip() + '\n'
                                print("Z-Drop removed           " + lines[zdrop_line].rstrip())
                                lines[zdrop_line] = '; Removed by FTC ' + lines[zdrop_line].rstrip() + '\n'
                        print('z-lift                   ' + str(zlift))

                        new_toolchange_gcode = (lines[toolchange_line].rstrip() + ' ' + move_x + ' ' + move_y + ('' if zlift == 0 else ' Z' + str(zlift))).rstrip()
                        print('parameter added          ' + new_toolchange_gcode)
                        lines[toolchange_line] = new_toolchange_gcode + '\n'
                        print('Horizontal move removed  ' + lines[move_line].rstrip().replace("  ", " "))
                        lines[move_line] = '; Removed by FTC ' + lines[move_line].rstrip().replace("  ", " ") + '\n'

                        if retraction_line > 0 and extrusion_line > 0:
                            print("Retraction move removed  " + lines[retraction_line].rstrip())
                            lines[retraction_line] = '; Removed by FTC ' + lines[retraction_line].rstrip() + '\n'
                            print("Extrusion move removed   " + lines[extrusion_line].rstrip())
                            lines[extrusion_line] = '; Removed by FTC ' + lines[extrusion_line].rstrip() + '\n'

                        print("\n")
            # write file
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
