import sys

def print_and_exit(s = "", err_code = 1):
    print >> sys.stderr, s
    sys.exit(err_code)
