#!/usr/bin/python

import sys, math
from optparse import OptionParser

import util.histogram
import numpy

def trimEdges(samples):
  keys = sorted(samples.keys())
  #remove zero stack distance (originally negative or zero)
  if keys[0] == 0:
    keys = keys[1:]
  
  # remove outliers
  median = keys[len(keys)/2]
  #filtered = [x for x in keys if abs(x-median) < (median*10)]
  filtered = [x for x in keys if x < 500]
  filtered = samples
  
  
  ret = {}
  for key in filtered: 
    ret[key] = samples[key]
  return ret

def processBins(samples, no_bins):
  trimmed = trimEdges(samples)
  
  keys = sorted(trimmed.keys())
  bin_size = (keys[-1] - keys[0]) / no_bins

#  ret = {}
#  for i in range(no_bins):
#    ret[i*bin_size] = lambda x: 
  weights, coords = numpy.histogram(trimmed.keys(), bins=no_bins, weights=trimmed.values())
  
  ret = {}
  for i in range(no_bins): 
    ret[coords[i]] = weights[i]
  
  return ret

def print_to_gnuplot(samples):
  for bin in sorted(samples.keys()): 
    print bin, samples[bin]

def main():
  usage = "usage: %prog [options] arg"
  parser = OptionParser(usage)
  
  parser.add_option("-f", "--dejavu",     dest="file")
  parser.add_option("-m", "--mode",     dest="mode")
  #  parser.add_option("-s", "--cache-size", dest="cache_size", default="".join( [ ", %i" % 2**x for x in range(10,22) ] ))
  #parser.add_option("-z", "--no_samples", dest="no_samples", default="1000")
  options, args = parser.parse_args()

#  ns = int(options.no_samples)
#  cs = [ int(x) for x in options.cache_size.split(',')[1:] ]
#  print cs

  try: 
    if options.mode.lower() == "dejavu":
      #print "set to dejavu"
      import proto.dejavu_pb2
      profile = proto.dejavu_pb2.Profile()
    elif options.mode.lower() == "pin":
      import proto.pincode_pb2
      profile = proto.pincode_pb2.Profile()
    else:
      raise AttributeError
  except AttributeError:
    print "invalid mode (-m), must be 'dejavu' or 'PIN'"
    exit()
  
  profile.ParseFromString(open(options.file).read())
  
  #w2p_list = [ w.pid for w in profile.window ]

  h = util.histogram.Histogram()
  no_samples, windows, avg = h.load(profile.sample, skip=0)
  print 'total samples:', no_samples
  #print '\noverall stats: \n', avg
  #print '\nwindows:'
  #for window in windows.keys(): 
  #  print window, windows[window], '\n'
  
  #print_to_gnuplot(avg)
  #print ''
  print_to_gnuplot(processBins(avg, 20))
  
#  for i in cs:
#    print '%i %f' % (i, util.miss_ratio.miss_ratio_rnd(h.avg, i / 64) * 100.0)



if __name__ == "__main__":
  main()

