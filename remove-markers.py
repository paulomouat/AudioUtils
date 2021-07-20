#!/usr/bin/env python3

import sys, getopt
import librosa
import numpy as np
from wavfile import read, write
from wavfileinfo import outputinfo

def usage():
    print('remove-markers.py -i <inputfile> -o <outputfile>')
    sys.exit(2)

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "i:o:", ["inputfile=", "outputfile="])
    except getopt.GetoptError:
        usage()
    
    for opt, arg in opts:
        if opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg

    if inputfile == '' or outputfile == '':
        usage()

    (targetrate, data, bits, *other) = read(inputfile)
    write(outputfile, targetrate, data, bits)

    print('output file:')
    outputinfo(outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])