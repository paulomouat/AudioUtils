#!/usr/bin/env python3

import sys, getopt
import librosa
import numpy as np
from wavfile import read, write
from wavfileinfo import outputinfo

def usage():
    print('slices.py -i <inputfile> -m <markerfile> -f <markerformat>')
    sys.exit(2)


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

    data, rate = librosa.load(inputfile, sr=None)
    print('input file:')
    outputinfo(inputfile)

    times = librosa.onset.onset_detect(y=data, sr=rate, hop_length=16, backtrack=True, units='time')
    print('with backtracking', times)
    samples = librosa.onset.onset_detect(y=data, sr=rate, hop_length=16, backtrack=True, units='samples')
    print('with backtracking', samples)

    topdb = 60
    framelength = 512 # 2048
    hoplength = 16 # 512
    intervals = librosa.effects.split(y=data, top_db=topdb, frame_length = framelength, hop_length=hoplength)
    print('intervals', topdb, intervals)
    print('intervals', topdb, intervals/rate)

if __name__ == "__main__":
   main(sys.argv[1:])