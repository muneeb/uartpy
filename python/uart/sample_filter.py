#!/usr/bin/python

r"""Generate sample filter functions from strings.

The filter module is used to generate sample filters from strings. A
compiled sample filter is a function object taking the parameters pc1,
pc2 and rdist. E.g.: lambda pc1, pc2, rdist: True

The filter language is really Python with some extra bells and
whistles. To make filter creation more convenient, filter
definitions are evaluated in a context with the helper
functions in the _filter_functions class.

Two functions are provided to compile filter strings, from_str()
and from_cmd_opt(), the only difference between the two is that
the latter does error handling suitable for command line option
handling.

The usage() function may be used to display filter language
documentation, e.g. upon calling a tool with the --help-filters
option.
"""

__version__ = "$Revision: 811 $"

import sys
import inspect
import collections

RDIST_DANGLING = sys.maxint

class _filter_functions:
    @staticmethod
    def all():
        r"""
        Create a filter allows all accesses to pass.
        """

        return lambda pc1, pc2, rdist: True

    @staticmethod
    def none():
        r"""
        Create a filter allows no accesses to pass.
        """

        return lambda pc1, pc2, rdist: False

    @staticmethod
    def pc1_range(start, stop):
        r"""
        Create a filter for a range of begin event PCs.
        """

        return lambda pc1, pc2, rdist: (pc1.pc >= start and pc1.pc <= stop)

    @staticmethod
    def pc2_range(start, stop):
        r"""
        Create a filter for a range of end event PCs.
        """

        return lambda pc1, pc2, rdist: (pc2 != None and
                                        pc2.pc >= start and pc2.pc <= stop)

    @staticmethod
    def pc1(pc):
        r"""
        Create a filter that selects a specific begin event PC. The
        specified PC may be either an integer or an iterable
        containing integers.
        """

        if isinstance(pc, collections.Sequence):
            return lambda pc1, pc2, rdist: pc1.pc in pc
        else:
            return lambda pc1, pc2, rdist: pc1.pc == pc

    @staticmethod
    def pc2(pc):
        r"""
        Create a filter that selects a specific end event PC. The
        specified PC may be either an integer or an iterable
        containing integers.
        """

        if isinstance(pc, collections.Sequence):
            return lambda pc1, pc2, rdist: pc2 and pc2.pc in pc
        else:
            return lambda pc1, pc2, rdist: pc2 and pc2.pc == pc

    @staticmethod
    def is_dangling():
        r"""
        Create a filter that selects all dangling samples.
        """

        return lambda pc1, pc2, rdist: rdist == RDIST_DANGLING and not pc2

    @staticmethod
    def is_nta():
        r"""
        Creates a filter that selects all NTA patched samples.
        """

        return lambda pc1, pc2, rdist: rdist == RDIST_DANGLING and pc2

    @staticmethod
    def and_(*args):
        r"""
        Create a filter that performs a logical 'and' of all its
        filter arguments. Filters are called in order and the
        evaluation is short-circuited if any of the filters return
        false.
        """

        def do_and(pc1, pc2, rdist):
            for c in args:
                if not c(pc1, pc2, rdist):
                    return False
            return True

        return do_and if args else none()

    @staticmethod
    def or_(*args):
        r"""
        Create a filter that performs a logical 'or' of all its
        filter arguments. Filters are called in order and the
        evaluation is short-circuited if any of the filters return
        true.
        """

        def do_or(pc1, pc2, rdist):
            for c in args:
                if c(pc1, pc2, rdist):
                    return True
            return False

        return do_or if list else none()

    @staticmethod
    def not_(operand):
        r""" 
        Creates a filter that performs the logical 'not' of its
        filter argument.
        """

        return lambda pc1, pc2, rdist: not operand(pc1, pc2, rdist)


def _get_filter_functions():
    for name, obj in inspect.getmembers(_filter_functions):
        if not name.startswith("_"):
            yield (name, obj)


def from_str(filter):
    r"""
    Creates a filter function from a filter description. The filter
    description is a piece of Python code that evaluates to a
    functions object. The code is executed in an environment with the
    helper functions in the _filter_functions class.
    """

    filter_globals = dict(_get_filter_functions())

    return eval(filter, filter_globals)

def from_cmd_opt(filter):
    r"""
    Like creates a filter function from a string. Unlike
    filter_from_str, this function does some rudimentary error
    handling that is suitable might be suitable when evaluating a
    filter from a command line option.
    """

    try:
        return from_str(filter)
    except Exception, e:
        print >> sys.stderr, "Invalid filter specification: %s" % e
        sys.exit(1)

def usage(out=sys.stdout):
    r"""
    Print a usage string for the filter mini-language. Suitable output
    for '--help-filters'.
    """

    print >> out, \
r"""
Filters are Python code snippets that are evaluated using eval in a
filter environment. To specify a custom filters may be specified as
lambda functions. For example:

lambda pc1, pc2, rdist: rdist > 42

pc1 and pc2 are pyusf.Access objects.

The following filters are predefined and may be used right away:
"""

    for name, func in _get_filter_functions():
        args, varargs, varkw, defaults = inspect.getargspec(func)
        arg_str = inspect.formatargspec(args, varargs, varkw, defaults)
        print >> out, "%s%s:" % (name, arg_str)
        print >> out, inspect.getdoc(func)
        print