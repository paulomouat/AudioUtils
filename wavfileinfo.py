from wavfile import read

def output(listname, list):
    size = len(list)
    print(listname)
    print(list[:min(10, size)]) if size > 0 else print('[]')

def outputinfo(inputfile):
    (rate, data, bits, cue, markers, *other) = read(inputfile, readmarkers=True, readmarkerslist=True)
    print('input file:', inputfile)
    print('rate:', rate, 'bits:', bits, 'dtype:', data.dtype)
    print('size:', data.size, 'shape:', data.shape)
    output('cue points:', cue)
    output('markers:', markers)
