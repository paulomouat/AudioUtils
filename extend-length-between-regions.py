import sys, getopt
import numpy as np
from wavfile import read, write
from wavfileinfo import outputinfo

def usage():
    print('extend-length-between-regions.py -i <inputfile> -o <outputfile>')
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

    double = True

    (rate, data, bits, cue, markers, unsupported, *other) = read(inputfile, readmarkers=True, readmarkerslist=True, readunsupported=True)
    print('input file:')
    outputinfo(inputfile)

    segments = np.split(data, cue)
    segmentslen = len(segments)
    print('there are', segmentslen, 'segments')

    if not double:
        sys.exit()

    doubleds = []

    for idx, segment in enumerate(segments):
        doubleds.append(segment)
        if idx > 0:
            size = int(segment.size/2)
            prevregion = markers[idx-1]
            rlength = prevregion['length']
            space = np.zeros_like(segment)[:size - rlength]
            doubleds.append(space)
        else:
            space = np.zeros_like(segment)
            doubleds.append(space)
    
    doubledmarkers = []

    pos = 0
    for idx, doubled in enumerate(doubleds):
        size = int(doubled.size/2)
        pos = pos + size
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