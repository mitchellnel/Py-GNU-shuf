"""
Generate random permutations

A Python 3 implementation of the GNU Coreutils-8.29 shuf command
"""

import sys, random, argparse


class shuf:

    def __init__(self, head_count, repeat_flag, lines, filename=""):
        self.head_count = head_count
        self.repeat_flag = repeat_flag

        # Consider 3 cases: both -i is not passed and no filename is passed,
        #   a filename is passed only, -i is passed only
        if (filename == "" or filename == "-") and lines == []:
            # neither -i nor filename passed --> read from stdin
            self.lines = []
            for line in sys.stdin:
                self.lines.append(line)
        elif len(lines) == 0:
            # filename passed only --> read from file
            file = open(filename, 'r')
            self.lines = file.readlines()
            file.close()
        else:
            # -i passed only, lines already has appropriate content
            self.lines = lines

    def shuffle_and_write(self):
        random.shuffle(self.lines)

        # Consider 4 cases: both -n and -r passed, -n passed only, -r passed
        #   only, neither -n or -r passed
        if self.head_count and self.repeat_flag:
            # perform random sampling with replacement a total of head_count
            #   times, then write sample to stdout
            for i in range(self.head_count):
                sys.stdout.write(random.choice(self.lines))
        elif not self.head_count and self.repeat_flag:
            # generate random permutations of lines and write to stdout forever
            while True:
                for i in range(len(self.lines)):
                    sys.stdout.write(self.lines[i])
                random.shuffle(self.lines)
        elif self.head_count and not self.repeat_flag:
            # write the first head_count lines of the shuffles lines to stdout
            for i in range(self.head_count):
                if self.head_count == len(self.lines):
                    break
                sys.stdout.write(self.lines[i])
        else:
            # just write all of lines shuffled to stdout
            for i in range(len(self.lines)):
                sys.stdout.write(str(self.lines[i]))


def main():
    prog_msg = __file__
    description_msg = "Write a random permutation of the input lines to " \
                      "standard output\n\n" \
                      "With no FILE, or when FILE is -, read standard input."
    usage_msg = __file__ + " [OPTION]... [FILE]\n  or: " + __file__ + " -i " \
                                                                      "LO-HI [OPTION]..."
    parser = argparse.ArgumentParser(prog=prog_msg, description=description_msg,
                                     usage=usage_msg)

    # Positional arguments
    parser.add_argument("FILE", nargs='?', default="")

    # Optional arguments
    parser.add_argument("-n", "--head-count", metavar="COUNT", type=int,
                        help="output at most COUNT lines")
    parser.add_argument("-r", "--repeat", action="store_true",
                        help="output lines can be repeated")
    parser.add_argument("-i", "--input-range", metavar="LO-HI",
                        help="treat each number LO through HI as an input line")

    # Get args (positional and optional) from parser
    args = parser.parse_args()

    # -i and FILE arguments are mutually exclusive
    if args.input_range and args.FILE:
        parser.error("-i/--input-range not allowed with argument FILE")

    # -n checks: head_count must be int, head_count must be non-negative
    try:
        if args.head_count is not None:  # checking for not None (using "is not None" makes it explicit)
            head_count = int(args.head_count)
    except TypeError as err:
        parser.error("invalid COUNT: {0}".format(args.head_count))

    if args.head_count is not None and args.head_count < 0:
        parser.error("negative COUNT: {0}".format(args.head_count))

    # -i checks: input_range must be string, '-' must be in input_range,
    #   input_range must have at least 3 characters (LO, -, HI for range LO-HI)
    try:
        input_range = args.input_range
    except ValueError as err:
        parser.error("invalid LO-HI input range: {0}".format(args.input_range))

    if input_range is not None and '-' not in input_range:
        parser.error("invalid LO-HI input range, no '-' delimiter: {0}"
                     .format(input_range))

    if input_range is not None and len(input_range) < 3:
        parser.error("invalid LO-HI input range: {0}".format(input_range))

    # -r checked by ArgParser

    # FILE has default value and will be checked when creating shuffler

    # Handle -i argument
    if input_range is not None:
        lo_hi_nums = input_range.split('-')

        # check that these elements are ints
        try:
            low = int(lo_hi_nums[0])
            high = int(lo_hi_nums[1])
        except TypeError as err:
            parser.error("invalid LO-HI input range, LO & HI must be ints: {0}"
                         .format(input_range))

        # check that 0 <= LO <= HI
        if not low >= 0 or not high >= low:
            parser.error("invalid LO-HI input range, must have 0 <= LO <= HI: {0}"
                         .format(input_range))

        # create list of size HI-LO+1 and fill with values from LO to HI
        #   inclusive of both
        num_list = []
        for i in range(low, high + 1):
            num_list.append(str(i) + '\n')

        # create shuf object and shuffle lines
        try:
            shuffler = shuf(args.head_count, args.repeat, num_list)
        except IOError as err:
            errno, strerror = err.args
            parser.error("I/O error({0}): {1}".format(errno, strerror))
    else:   # no -i argument
        # use stdin or FILE
        # create shuf object and shuffle lines
        if args.FILE == "" or args.FILE == '-':
            try:
                shuffler = shuf(args.head_count, args.repeat, [])
            except IOError as err:
                errno, strerror = err.args
                parser.error("I/O error({0}): {1}".format(errno, strerror))
        else:
            try:
                shuffler = shuf(args.head_count, args.repeat, [], args.FILE)
            except IOError as err:
                errno, strerror = err.args
                parser.error("I/O error({0}): {1}".format(errno, strerror))

    # shuffle lines
    shuffler.shuffle_and_write()


if __name__ == "__main__":
    main()
