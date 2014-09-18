#!/usr/bin/python


import sys, math
from optparse import OptionParser

sys.path.append("..")

import util.histogram
import util.miss_ratio

import proto.pincode_pb2
import proto.scarphase_pb2

import numpy as np

if __name__ == "__main__":
  
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    
    parser.add_option("-d", "--dejavu",     dest="dejavu")
    parser.add_option("-l", "--line-size",  dest="line_size", default="64")
    parser.add_option("-s", "--cache-size", dest="cache_size", default="".join( [ ", %i" % 2**x for x in range(10,22) ] ))
    #parser.add_option("-z", "--no_samples", dest="no_samples", default="1000")
    options, args = parser.parse_args()

    ls = int(options.line_size)
    #ns = int(options.no_samples)
    cs = [ int(x) for x in options.cache_size.split(',')[1:] ]
    
    profile = proto.pincode_pb2.Profile()
    profile.ParseFromString(open(options.dejavu).read())
    
    #w2p_list = [ w.pid for w in profile.window ]
    w2p_list = []
    for i in range(2000):
      w2p_list.append(0)
    
    h = util.histogram.Histogram()
    no_samples, windows, avg = h.load(profile.sample, skip=0)
    
    print 'to_no_samples = %li' % no_samples
    
    for i in cs:
        print '%i %f' % (i, util.miss_ratio.miss_ratio_rnd(avg, i / ls) * 100.0)
        
   
