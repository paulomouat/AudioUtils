import sys, getopt
import numpy as np
from wavfile import read, write

def output(list):
    size = len(list)
    print(list[:min(10, size)]) if size > 0 else print('[]')

def usage():
    print('extend-silence.py -i <inputfile> -o <outputfile>')
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
    print('input file:', inputfile)
    print('rate:', rate, 'bits:', bits, 'dtype:', data.dtype)
    print('size:', data.size, 'shape:', data.shape)
    output(cue)
    output(markers)
    output(unsupported)

    segments = np.split(data, cue)
    segmentslen = len(segments)
    print('there are', segmentslen, 'segments')

    idx = 0
    for segment in segments:
        size = int(segment.size/2)
        #print(idx, size)
        idx = idx + 1

    if not double:
        sys.exit()

    doubleds = []

    idx = 0
    for segment in segments:
        size = int(segment.size/2)
        #print(idx, size)
        doubleds.append(segment)
        space = np.zeros_like(segment)
        doubleds.append(space)
        idx = idx + 1

    doubledmarkers = []

    pos = 0
    idx = 0
    for doubled in doubleds:
        size = int(doubled.size/2)
        pos = pos + size
        if idx % 2 == 1 and len(markers) > 0:
            marker = markers[0]
            markers.pop(0)
            doubledmarker = {'position': pos, 'label': marker["label"], 'length': marker["length"]}
            doubledmarkers.append(doubledmarker)
        idx = idx + 1

    doubleddata = np.concatenate(doubleds)

    write(outputfile, rate, doubleddata, bits, doubledmarkers)

    (rate, data, bits, cue, doubledmarkers, *other) = read(outputfile, readmarkers=True, readmarkerslist=True)
    print('output file:', outputfile)
    print('rate:', rate, 'bits:', bits, 'dtype:', data.dtype)
    print('size:', data.size, 'shape:', data.shape)
    output(cue)
    output(doubledmarkers)

if __name__ == "__main__":
   main(sys.argv[1:])