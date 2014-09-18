#!/usr/bin/python2.7
from optparse import OptionParser
import proto.dejavu_pb2 as dejavu

def main():
  usage = "usage: %prog -f <filename>"
  parser = OptionParser(usage)
  
  parser.add_option("-f", "--file",     dest="file")
  
  options, args = parser.parse_args()
             
  if not options.file:
    print usage
    return 1

  p = dejavu.Profile()
  p.ParseFromString(open(options.file).read())
  
  #print len(p.window)
  print p
  return 0


if __name__ == "__main__":
  main()

