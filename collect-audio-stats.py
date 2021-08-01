#!/usr/bin/env python3

# in order to use tee, stdout needs to be forced to be unbuffered:
# python3 -u collect-audio-stats.py | tee output.txt

import glob
import subprocess
from pathlib import Path, PurePath

files = []
wavs = glob.glob('./**/*.wav', recursive=True)
files.extend(wavs)
flacs = glob.glob('./**/*.flac', recursive=True)
files.extend(flacs)
files.sort()

def print_stats(f, il, lra, dbtp):
  #print(f, il, lra, dbtp, sep='\t')
  print(f, dbtp, sep='\t')

# sample output of the r128x-cli command:
# FILE                                       IL (LUFS)    LRA (LU)  MAXTP (dBTP)
# chord 1.wav                                    -24.8       +15.4         -10.4

for f in files:
  command = '~/bin/r128x-cli ' + '"' + f + '"'
  p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
  path = PurePath(f)
  
  output = p.stdout
  lines = output.splitlines()
  last_line = lines[-1]
  if last_line.startswith("\x1b[F\x1b[J"):
    last_line = last_line[6:]
  
  file = path.name
  raw_stats = last_line[len(file):]
  stats = raw_stats.split()
  il = stats[0]
  lra = stats[1]
  dbtp = stats[2]

  print_stats(f, il, lra, dbtp)
