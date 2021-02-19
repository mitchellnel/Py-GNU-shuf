# Py-GNU-shuf
Python 3 implementation of the GNU shuf command (that is part of GNU Coreutils).

Options:
- -i LO-HI [--input-range] : treat each number LO through HI as an input line
  - e.g. -i 3-7 will print a random permutation of the numbers 3, 4, 5, 6, 7
- -n COUNT [--head-count] : output at most COUNT lines
- -r [--repeat] : output lines can be repeated (selection with replacement)

Invoking the --help option will provide information about the program's usage on the command line.
