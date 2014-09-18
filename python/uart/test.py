#!/usr/bin/python

class TestCaseError(Exception):
    def __init__(self, msg = ""):
        self.msg = msg

    def __str__(self):
        return self.msg

class TestCase:
    def __init__(self, name = ""):
        self.name = name
        self.tests = []
        self.log_ = {}
        self.running = ""
        self.failed = {}

    def init(self): pass
    def fini(self): pass

    def run(self):
        self.init()
        for attr in dir(self):
            if attr.find("test") == 0:
                f = getattr(self, attr)
                if callable(f):
                    test_name = attr
                    self.tests.append(test_name)
                    try:
                        self.running = test_name
                        self.log_[test_name] = ""
                        f()
                    except TestCaseError, e:
                        self.failed[test_name] = str(e)

        self.fini()
        self.print_result()
        return len(self.failed.keys())

    def print_result(self):
        for name in self.tests:
            print "-" * 40
            if not self.failed.has_key(name):
                print "PASSED: " + name
            else:
                print "FAILED: " + name,
                if self.failed[name] != "":
                    print "(" + msg + ")",
                print

                print self.log_[name]

        print "-" * 40
        print "%d tests passed" % (len(self.tests) - len(self.failed.keys()))
        print "%d tests failed" % (len(self.failed.keys()))

    def log(self, msg):
        self.log_[self.running] += msg

    def fail_if(self, cond, msg = ""):
        if cond:
            raise TestCaseError(msg)

