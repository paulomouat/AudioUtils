#!/usr/bin/env python3
 
import sys, getopt
import numpy as np
from wavfile import read, write
from wavfileinfo import outputinfo

def usage():
    print('extend-length-between-markers.py -i <inputfile> -o <outputfile> -f <factor>')
    sys.exit(2)

def main(argv):
    inputfile = ''
    outputfile = ''
    factoropt = ''

    try:
        opts, args = getopt.getopt(argv, "i:o:f:", ["inputfile=", "outputfile=", "factor="])
    except getopt.GetoptError:
        usage()
    
    for opt, arg in opts:
        if opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-f", "--factor"):
            factoropt = arg

    if inputfile == '' or outputfile == '':
        usage()

    factor = 1.0

    if factoropt != '':
        factor = float(factoropt)

    if factor < 1.0:
        print('the supplied factor needs to be at least 1.0')
        sys.exit(2)

    (rate, data, bits, cue, markers, *other) = read(inputfile, readmarkers=True, readmarkerslist=True)
    print('input file:')
    outputinfo(inputfile)

    segments = np.split(data, cue)
    segmentslen = len(segments)
    print('there are', segmentslen, 'segments')

    doubleds = []

    for idx, segment in enumerate(segments):
        length = segment.shape[0]
        num_channels = segment.shape[1]
        delta_length = int(length * factor) - length
        doubleds.append(segment)
        space = np.zeros_like(segment, shape=(delta_length, num_channels))
        doubleds.append(space)

    doubledmarkers = []

    pos = 0
    for idx, doubled in enumerate(doubleds):
        length = doubled.shape[0]
        pos = pos + length
        if idx % 2 == 1 and len(markers) > 0:
            marker = markers[0]
            markers.pop(0)
            doubledmarker = {'position': pos, 'label': marker["label"], 'length': marker["length"]}
            doubledmarkers.append(doubledmarker)

    doubleddata = np.concatenate(doubleds)

    write(outputfile, rate, doubleddata, bits, doubledmarkers)

    print('output file:')
    outputinfo(outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])