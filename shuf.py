#! /usr/bin/env python3
"""
Importing necessary librarires
"""
import random, sys
from optparse import OptionParser

"""
Define randline classes for file, stdin and -i lists
Each class has a function that chooses a line with or without
replacement depending on the -r option. There is a function
that determines the number of iterations depending on -n and
how many lines the file has and a function that determines
whether the function goes on forever.
"""
class randlinefile:
    def __init__(self, filename, repeatvar, numlines):
        f = open(filename, 'r')
        self.lines = f.readlines()
        f.close()
        self.repeatvar = repeatvar
        self.numlines = numlines

    def chooseline(self):
        if( self.repeatvar == True ):
            return random.choice(self.lines)
        else:
            output = random.choice(self.lines)
            self.lines.remove(output)
            return output

    def num_iter(self):
        if self.repeatvar:
            return self.numlines
        return min(self.numlines, len(self.lines))

    def go_on_forever(self):
        if self.numlines == sys.maxsize and self.repeatvar == True:
            return True
        else:
            return False

class randlinelist:
    def __init__(self, input_list, repeatvar, numlines):
        self.repeatvar = repeatvar
        self.numlines = numlines
        self.input_list = input_list

    def chooseline(self):
        if self.input_list == []:
            return '\n'
        if( self.repeatvar == True ):
            return random.choice(self.input_list)
        else:
            output = random.choice(self.input_list)
            self.input_list.remove(output)
            return output

    def num_iter(self):
        if self.repeatvar:
            return self.numlines
        return min(self.numlines, len(self.input_list))

    def go_on_forever(self):
        if self.numlines == sys.maxsize and self.repeatvar == True:
            return True
        else:
            return False

class randlineinput:
    def __init__(self, input_list, repeatvar, numlines):
        self.repeatvar = repeatvar
        self.numlines = numlines
        self.input_list = input_list

    def chooseline(self):
        if self.repeatvar == True:
            return random.choice(self.input_list)
        else:
            output = random.choice(self.input_list)
            self.input_list.remove(output)
            return output

    def go_on_forever(self):
        if self.numlines == sys.maxsize and self.repeatvar == True:
            return True
        else:
            return False

    def num_iter(self):
        if self.repeatvar:
            return self.numlines
        return min(self.numlines, len(self.input_list))

"""
Checking the formatting of the -i option
"""
def check_format(input_string):
    available_terms = ["1","2","3","4","5","6","7","8","9","0","-"]
    if input_string[0] == "0":
        return False
    if input_string[len(input_string)-1] == "-":
        return False
    for i in range(len(input_string)):
        if input_string[i] not in available_terms:
            return False
        if input_string[i] == "-":
            if input_string[i+1] == "-" or input_string[i+1] == "0":
                return False
    lo=0
    hi=0
    before_hyphen=True
    for i in range(len(input_string)):
        if input_string[i] == "-":
            before_hyphen = False
            continue
        elif(before_hyphen):
            lo = lo*10 + int(input_string[i])
        else:
            hi = hi*10 + int(input_string[i])
    if lo - hi > 1:
        return False
    return True
"""
Converting the -i option to a list
"""
def convert_to_list(input_string):
    lo=0
    hi=0
    target_list=[]
    before_hyphen=True
    for i in range(len(input_string)):
        if input_string[i] == "-":
            before_hyphen = False
            continue
        elif(before_hyphen):
            lo = lo*10 + int(input_string[i])
        else:
            hi = hi*10 + int(input_string[i])
    if lo - hi == 1:
        return []
    for j in range(lo, hi+1):
        target_list += [j]
    return target_list

"""
Main function with all options and their default values
There are a bunch of booleans in place to determine whehter
the final input is from stdin, a file or the range.
"""

def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE

Output randomly selected lines from FILE."""

    parser = OptionParser(version=version_msg, usage=usage_msg)

    parser.add_option("-n", "--head-count",
                      action="store", dest="numlines", default=sys.maxsize,
                      help="Output at most COUNT lines. By default all input lines are output")

    parser.add_option("-i", "--input-range",
                      action="store", dest="input_range", default="none",
                      help="Act as if input came from a file containing the range of unsigned decimal integers lo,..,hi one per line")

    parser.add_option("-r", "--repeat",
                      action="store_true", dest="repeatvar", default=False,
                      help="Repeat output values, that is select with replacement. Typically combined with --head_count; if --head-count is not given, shuf repeats indefinitely.")


    options, args = parser.parse_args(sys.argv[1:])
    readfromout = False

    try:
        numlines = int(options.numlines)
    except:
        parser.error("invalid COUNT: {0}".
                     format(options.numlines))

    if numlines < 0:
        parser.error("negative count: {0}".
                     format(numlines))
    if len(args) > 1:
        parser.error("wrong number of operands")

    try:
        repeatvar = bool(options.repeatvar)
    except:
        parser.error("invalid usage {0}".
                     format(options.repeatvar))

    try:
        input_range = str(options.input_range)
    except:
        parser.error("invalid input: {0}".
                     format(options.input_range))
    if args == ['-'] or (args == [] and input_range == "none"):
        readfromout = True

    if(input_range != "none" and len(args) != 0):
        parser.error("extra operand '{0}'".
                     format(args[0]))
    else:
        if(input_range != "none"):
            if(check_format(input_range) == False):
                parser.error("Improper formatting of range a-b")
            else:
                inRange = True
                inFile = False
                input_list = convert_to_list(input_range)
        else:
            if readfromout == False:
                input_file = args[0]
                inFile = True
                inRange = False
            else:
                inRange = False
                inFile = False
                """
                Create classes based on the file type and run all functions to determine
                the loop and how many times it runs.
                """
    if inRange:
        generator = randlinelist(input_list, repeatvar, numlines)
        infinite_loop = generator.go_on_forever()
        if infinite_loop:
            while(infinite_loop):
                output_string = str(generator.chooseline()) + "\n"
                sys.stdout.write(output_string)
        else:
            iterations = generator.num_iter()
            for index in range(iterations):
                output_string = str(generator.chooseline()) + "\n"
                sys.stdout.write(output_string)
    elif inFile:
        try:
            generator = randlinefile(input_file, repeatvar, numlines)
            infinite_loop = generator.go_on_forever()
            if infinite_loop:
                while(infinite_loop):
                    sys.stdout.write(generator.chooseline())
            else:
                iterations = generator.num_iter()
                for index in range(iterations):
                    sys.stdout.write(generator.chooseline())
        except IOError as e:
            errno, strerror = e.args
            parser.error("I/O error({0}): {1}".
                         format(errno, strerror))
    else:
        input_line = []
        for line in sys.stdin:
            input_line += [line]
        generator = randlineinput(input_line, repeatvar, numlines)
        infinite_loop = generator.go_on_forever()
        if infinite_loop:
            while infinite_loop:
                output_string = generator.chooseline()
                sys.stdout.write(output_string)
        else:
            iterations = generator.num_iter()
            for index in range(iterations):
                output_string = generator.chooseline()
                sys.stdout.write(output_string)

if __name__ == "__main__":
    main()
