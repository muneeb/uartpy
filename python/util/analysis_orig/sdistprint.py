#!/usr/bin/python
import sys
import math

from optparse import OptionParser

from uart.hist import Hist
import uart.sample_filter as sample_filter

import pyusf
import lrumodel
import utils

__version__ = "$Revision$"

class Conf:
    def __init__(self):
        parser = OptionParser("usage: %prog [OPTIONS...] INFILE")

        parser.add_option("-l", "--line-size",
                          type="int", default="64",
                          dest="line_size",
                          help="Use a specific line size.")

        parser.add_option("-f", "--filter",
                          type="str", default="all()",
                          dest="filter",
                          help="Filter for events to display in histogram.")

        parser.add_option("--help-filters",
                          action="callback", callback=self.help_filters,
                          help="Display help about the filter language.")


        (opts, args) = parser.parse_args()

        if opts.line_size <= 0 or \
                opts.line_size & (opts.line_size - 1) != 0:
            print >> sys.stderr, "Invalid line size specified."
            sys.exit(1)

        if len(args) == 0:
            print >> sys.stderr, "No input file specified."
            sys.exit(1)

        self.filter = sample_filter.from_str(opts.filter)
        self.ifile_name = args[0]
        self.line_size = opts.line_size

    def help_filters(self, option, opt, value, parser):
        sample_filter.usage()
        sys.exit(0)

def open_sample_file(file_name, line_size):
    try:
        usf_file = pyusf.Usf()
        usf_file.open(file_name)
    except IOError, e:
        print >> sys.stderr, "Error: %s" % str(e)
        sys.exit(1)

    if usf_file.header.flags & pyusf.USF_FLAG_TRACE:
        print >> sys.stderr, "Error: Specified file is a trace."
        sys.exit(1)

    if not usf_file.header.line_sizes & line_size:
        print >> sys.stderr, \
            "Eror: Specified line size does not exist in sample file."
        sys.exit(1)

    return usf_file

def generate_sdist_hist(burst_hists):
    hist = {}
    for (rdists, filtered_rdists) in burst_hists:
        r2s = lrumodel.lru_sdist(rdists)
        for (rdist, count) in filtered_rdists.items():
            sdist = r2s[rdist]
            hist[sdist] = hist.get(sdist, 0) + count

    return hist

def main():
    conf = Conf()
    usf_file = open_sample_file(conf.ifile_name, conf.line_size)
    burst_hists = utils.usf_read_events(usf_file,
                                        line_size=conf.line_size,
                                        filter=conf.filter)
    usf_file.close()

    hist = generate_sdist_hist(burst_hists)

    data = hist.items()
    data.sort(key=lambda x: x[0])

    l1_sd_samples = 0
    l2_sd_samples = 0
    l3_sd_samples = 0
    mem_sd_samples = 0
    non_l1_sd_samples = 0
    total_sd_samples = 0

    for (sd, count) in data:
#        print "%i %i" % (sd * conf.line_size, count)
        
        total_sd_samples += count
        if sd < 1024: # 1024 number of cache lines in 64kB L1 cache
            l1_sd_samples += count
            continue
        elif sd < 8192:
            l2_sd_samples += count
        elif sd < 98304:
            l3_sd_samples += count
        else:
            mem_sd_samples += count
            
        non_l1_sd_samples += count
                    
    l1_bound_samples = (float(l1_sd_samples)/float(total_sd_samples)*100)
    l2_bound_samples = (float(l2_sd_samples)/float(non_l1_sd_samples)*100)
    l3_bound_samples = (float(l3_sd_samples)/float(non_l1_sd_samples)*100)
    mem_bound_samples = (float(mem_sd_samples)/float(non_l1_sd_samples)*100)
    non_l1_bound_samples = (float(non_l1_sd_samples)/float(total_sd_samples) * 100)
    print "L1 %.2f %% of total"%(l1_bound_samples)
    print "L2 %.2f %% of %.2f %%"%(l2_bound_samples, non_l1_bound_samples)
    print "L3 %.2f %% of %.2f %%"%(l3_bound_samples, non_l1_bound_samples)
    print "Memory %.2f %% of %.2f %%"%(mem_bound_samples, non_l1_bound_samples)

if __name__ == "__main__":
    main()

