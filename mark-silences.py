#!/usr/bin/env python3

import sys, getopt
import librosa
import numpy as np
from wavfile import read, write
from wavfileinfo import outputinfo

def usage():
    print('mark-silences.py -i <inputfile> -o <outputfile>')
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

    data, rate = librosa.load(inputfile, sr=None)
    print('input file:')
    outputinfo(inputfile)

    topdb = 55
    framelength = 512 # 2048
    hoplength = 16 # 512
    intervals = librosa.effects.split(y=data, top_db=topdb, frame_length = framelength, hop_length=hoplength)
    print('intervals', topdb, intervals)
    print('intervals', topdb, intervals/rate)

    (targetrate, data, bits, *other) = read(inputfile)

    ratefactor = targetrate/rate

    markers = []
    for idx, interval in enumerate(intervals):
        start = int(interval[0] * ratefactor)
        end = int(interval[1] * ratefactor)
        marker = {'position': start, 'label': b'Marker ' + bytes(str(idx + 1), 'UTF-8'), 'length': end - start}
        markers.append(marker)

    write(outputfile, targetrate, data, bits, markers)

    print('output file:')
    outputinfo(outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])