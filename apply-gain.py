#!/usr/bin/env python3
 
import sys, getopt
import numpy as np
from wavfile import read, write
from wavfileinfo import outputinfo

def usage():
    print('apply-gain.py -i <inputfile> -o <outputfile> -g <gain>')
    sys.exit(2)

def db_to_float(db, using_amplitude=True):
    db = float(db)
    if using_amplitude:
        return 10 ** (db / 20)
    else:  # using power
        return 10 ** (db / 10)

def main(argv):
    inputfile = ''
    outputfile = ''
    gainopt = ''

    try:
        opts, args = getopt.getopt(argv, "i:o:g:", ["inputfile=", "outputfile=", "gain="])
    except getopt.GetoptError:
        usage()
    
    for opt, arg in opts:
        if opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-g", "--gain"):
            gainopt = arg

    if inputfile == '' or outputfile == '':
        usage()

    gain = 0.0

    if gainopt != '':
        gain = float(gainopt)

    gain_float = db_to_float(gain)

    (rate, data, bits, *other) = read(inputfile)
    print('input file:')
    outputinfo(inputfile)

    scaled_data = data * gain_float

    write(outputfile, rate, scaled_data, bits)

    print('output file:')
    outputinfo(outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])