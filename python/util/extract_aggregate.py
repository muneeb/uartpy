#!/usr/bin/python

import sys, math, os
from optparse import OptionParser

import util.histogram
import numpy

import subprocess

verbose = False

def trimEdges(samples, trim_lower, trim_upper):
  keys = sorted(samples.keys())
  #remove zero stack distance (originally negative or zero)
  #if keys[0] == 0:
  #  keys = keys[1:]
  counter = 0
  while keys[0] <= trim_lower:
    keys = keys[1:]
    counter+=1
  if verbose == True:
    print "trimmed on the lower bound: ", counter, "stack distances"
  #keys = keys[2000:]
  
  # remove outliers
  #median = keys[len(keys)/2]
  #filtered = [x for x in keys if abs(x-median) < (median*10)]
  filtered = [x for x in keys if x < trim_upper]
  if verbose == True: 
    print "trimmed on the upper bound: ", len(keys)-len(filtered), "stack distances"
  
  ret = {}
  for key in filtered: 
    ret[key] = samples[key]
  return ret

def processBins(samples, no_bins, cumulative, trim_lower, trim_upper):
  #trimmed = trimEdges(samples, trim_lower, trim_upper)
  trimmed = samples
  
  keys = sorted(trimmed.keys())
  bin_size = (keys[-1] - keys[0]) / no_bins

#  ret = {}
#  for i in range(no_bins):
#    ret[i*bin_size] = lambda x: 
  
  '''
  if cumulative == True:
    #ret = [x for i, x in enumerate(trimmed.values()) if i % (float(len(trimmed.values()))/no_bins) < 1.0]
    ret = []
    div = (float(len(trimmed.values()))/no_bins)
    for i, key in enumerate(sorted(trimmed)):
      if i % div < 1.0:
        ret.append(trimmed[key])
  else: 
    weights, coords = numpy.histogram(trimmed.keys(), bins=no_bins, weights=trimmed.values())
    ret = {}
    for i in range(no_bins): 
      ret[coords[i]] = weights[i]
  '''
  weights, coords = numpy.histogram(trimmed.keys(), bins=no_bins, weights=trimmed.values())
  ret = {}
  for i in range(no_bins): 
    ret[coords[i]] = weights[i]
  if cumulative == True:
    nsamples = sum(ret.values())
    acc = 0
    for i, key in enumerate(sorted(ret.keys())):
    #for key in aggregate.keys():
      t = (100.0*ret[key])/nsamples
      #tmp = ret[key]
      ret[key] = float(t + acc)
      acc = float(ret[key])
      #print key, float(i+1)/len(ret.keys()), tmp, acc
  return ret





def print_to_gnuplot(samples, cumulative, draw):
  #if cumulative == True: 
  #  for i, v in enumerate(samples):
  #    print i, v
  #else: 
  if (draw == False):
    for key in sorted(samples):
      print key, samples[key]
  else:
    f = open('../gnuplot/data.dat', 'w')
    for key in sorted(samples):
      #print >> f, key, samples[key]
      f.write(str(key) + " " + str(samples[key]) + "\n")
    f.close()
    subprocess.call("cd ../gnuplot && ./draw_plot.sh", shell=True)




def get_gnuplot_output(no_bins, cumulative, mode, directory, trim_lower, trim_upper, draw):
  
  try:
    filenames = os.listdir(directory)
  except OSError:
    filenames = [os.path.basename(directory)]
    directory = os.path.dirname(directory)
  aggregate = {}
  
  samples_list = []
  
  for filename in filenames: 
  
    if (mode == "pin"):
      import proto.pincode_pb2
      profile = proto.pincode_pb2.Profile()
    elif (mode == "dejavu"):
      import proto.dejavu_pb2
      profile = proto.dejavu_pb2.Profile()
    else: 
      print "invalid mode"
      exit()
    profile.ParseFromString(open(os.path.join(directory, filename)).read())
    
    #w2p_list = [ w.pid for w in profile.window ]

    h = util.histogram.Histogram()
  
    no_samples, windows, avg = h.load(profile.sample, skip=0)
    
    samples_list.append(no_samples)
    
    for key in avg.keys():
      try: 
        aggregate[key] += avg[key]
      except KeyError:
        aggregate[key] = avg[key];

  if verbose == True:
    print samples_list
    print "total samples:", sum(samples_list)
    print "avg:", numpy.mean(samples_list)
    print "stddev:", numpy.std(samples_list)
  
  
  aggregate = trimEdges(aggregate, trim_lower, trim_upper)
  print "total samples after trimming:", sum(aggregate.values())
  if cumulative == True: 
    None
    '''
    nsamples = sum(aggregate.values())
    acc = 0
    for i, key in enumerate(sorted(aggregate.keys())):
    #for key in aggregate.keys():
      t = (100.0*aggregate[key])/nsamples
      tmp = aggregate[key]
      aggregate[key] = float(t + acc)
      acc = float(aggregate[key])
      print key, float(i+1)/len(aggregate.keys()), tmp, acc
    '''
  else: 
    for key in aggregate.keys():
      aggregate[key] = float(aggregate[key])/len(filenames)
      #aggregate[key] = int(aggregate[key])
  print_to_gnuplot(processBins(aggregate, no_bins, cumulative, trim_lower, trim_upper), cumulative, draw)




def main():
  usage = "usage: %prog [options] arg"
  parser = OptionParser(usage)
  
  parser.add_option("-m", "--mode",     dest="mode")
  parser.add_option("-f", "--folder", dest="directory", default='dpb')
  parser.add_option("-c", "--cumulative", action="store_true", dest="cumulative", default=False)
  parser.add_option("-b", "--bins", type="int", dest="no_bins", default=20)
  parser.add_option("-l", "--min-stack-distance", type="int", dest="trim_lower", default=-1)
  parser.add_option("-u", "--max-stack-distance", type="int", dest="trim_upper", default=100000000000)
  parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)
  parser.add_option("-d", "--draw", action="store_true", dest="draw", default=False)
  options, args = parser.parse_args()
  
  try: 
    if options.mode.lower() == "dejavu":
      #print "set to dejavu"
      None
    elif options.mode.lower() == "pin":
      #print "set to PIN"
      None
    else:
      raise AttributeError
  except AttributeError:
    print "invalid mode (-m), must be 'dejavu' or 'PIN'"
    exit()

  global verbose
  verbose = bool(options.verbose)
  get_gnuplot_output(no_bins = int(options.no_bins), cumulative = bool(options.cumulative), mode = options.mode.lower(), directory=options.directory, trim_lower = int(options.trim_lower), trim_upper = int(options.trim_upper), draw = bool(options.draw))
  

if __name__ == "__main__":
  main()

