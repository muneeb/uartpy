################################################################################
#!/usr/bin/python

import os, sys, copy, math
import proto.dejavu_pb2 as dejavu

################################################################################

class Histogram():
    
  def __init__(self):
    self.window = {}
    self.phase  = {}
    self.avg    = {}
  
  def load(self, samples, skip):
    no_samples = 0
    for i,s in enumerate(sorted(samples, key=lambda x: x.access[0].time)):
      if (len(s.access) == 1): # this gets rid of the extra long reuse distances that timed out in PIN. 
        continue # dejavu takes care of those in the code itself, so they're not logged anyway. 
        #pass
      start = s.access[0]
      end = s.access[-1]
      
      if skip > 0:
        if i % skip == 0:
          pass
        else:
          continue
          
      # The reuse distance
      rd = end.time - start.time

      if rd < 0:
        rd = 0
      

      # Add histogram for the new phase
      if not start.wid in self.window:
        self.window[start.wid] = {}
      
      pwin = self.window[start.wid]

      # Record the reuse
      if rd in pwin:
        pwin[rd] += 1
      else:
        pwin[rd]  = 1
      
      # Add the reuse to the average
      if rd in self.avg:
        self.avg[rd] += 1
      else:
        self.avg[rd]  = 1
        
      no_samples += 1
    
    return no_samples, self.window, self.avg

################################################################################

