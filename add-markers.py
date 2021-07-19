#!/usr/bin/env python3

import sys, getopt
import numpy as np
import csv
from decimal import Decimal
from wavfile import read, write
from wavfileinfo import outputinfo

def usage():
    print('add-markers.py -i <inputfile> -o <outputfile> -m <markerfile> -f <markerformat>')
    sys.exit(2)

def readmarkers(inputfile, rate):
    _markers = []
    with open(inputfile, 'r') as f:
        # audacity format processing:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            position = int(Decimal(row[0]) * rate)
            end = int(Decimal(row[1]) * rate)
            length = end - position
            label = row[2].encode()
            _markers.append({'position': position, 'label': label, 'length': length})
    return _markers

def main(argv):
    inputfile = ''
    outputfile = ''
    markerfile = ''
    markerformat = ''

    try:
        opts, args = getopt.getopt(argv, "i:o:m:f:", ["inputfile=", "outputfile=", "markerfile=", "markerformat="])
    except getopt.GetoptError:
        usage()
    
    for opt, arg in opts:
        if opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-m", "--markerfile"):
            markerfile = arg
        elif opt in ("-f", "--markerformat"):
            markerformat = arg

    if inputfile == '' or outputfile == '' or markerfile == '':
        usage()

    if markerformat == '':
        markerformat = 'audacity'

    (rate, data, bits, oldmarkers, *other) = read(inputfile, readmarkerslist=True)
    print('input file:')
    outputinfo(inputfile)

    rawmarkers = readmarkers(markerfile, rate)
    print('read', len(rawmarkers), 'from marker file', markerfile)

    markers = [m for m in rawmarkers if m['position'] < data.shape[0]]
    print('found', len(markers), 'applicable markers based on length of output file', outputfile)

    write(outputfile, rate, data, bits, markers)

    print('output file:')
    outputinfo(outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])