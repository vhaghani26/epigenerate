#!/usr/bin/env python3

import argparse
import time
import sys
import os
import stat

####################
## Argparse Setup ##
####################

# Initialize argparse
parser = argparse.ArgumentParser(
    description='Find duplicated files within the specified directory')

# Required arguments
parser.add_argument('--path', required=True, type=str,
    metavar='<str>', help='Path to directory')
    
# Optional arguments
parser.add_argument('--min', required=False, default = 1024, type=int, 
    metavar='<min size>', help='Minimum file size [%(default)s]')

parser.add_argument('--bytes', required=False, default = 128, type=int,
    metavar='<int>', help='Number of bytes to read for pseudo-checksum [%(default)s]')
    
# Switch
parser.add_argument('--verbose', action="store_true",
   help='Enables print out of script progress')

# Finalization of argparse
arg = parser.parse_args()

# Initiate timer
t0 = time.time()

#################
## Verify Path ##
#################

isExist = os.path.exists(arg.path)
if not isExist:
    raise AssertionError(f"No such file or directory {arg.path}")

#########################
## Retrieve File Sizes ##
#########################

if arg.verbose:
    print("Scanning all subdirectories and files and recording sizes...", file = sys.stderr)
    
# Index all files by their size
size = {}
for path, subdirs, files in os.walk(arg.path):
    for name in files:
        filepath = os.path.join(path, name)
        # Avoid user-specific paths in HPCs and software-package related files
        if ("usr" not in filepath) and ("conda" not in filepath) and ("rlibs" not in filepath) and ("bin" not in filepath):
            mode = os.lstat(filepath).st_mode
            if not stat.S_ISREG(mode): continue
            s = os.path.getsize(filepath)
            if s < arg.min: continue
            if s not in size: size[s] = []
            size[s].append(filepath)

#####################
## Find Duplicates ##
#####################

if arg.verbose:
    print("Calculating psuedo-checksum for potentially duplicated files...", file = sys.stderr)
        
# Find duplicate files (1) by file size (2) by pseudo-checksum
for s in sorted(size, reverse=True):    
    if len(size[s]) == 1: continue
    
    # Create a pseudo-checksum by looking at the head and tail of a file
    pseudosum = {}
    for filepath in size[s]:
        with open(filepath, mode='rb') as fp:
            head = fp.read(arg.bytes)
            fp.seek(-arg.bytes, 2)
            tail = fp.read(arg.bytes)
            sig = (head, tail)
            if sig not in pseudosum: pseudosum[sig] = []
            pseudosum[sig].append(filepath)
    
    # Report duplicates
    for sig in pseudosum:
        if len(pseudosum[sig]) == 1: continue
        ps = None
        if   s > 1e12: ps = f'{s/1e12:.2f}T'
        elif s > 1e9:  ps = f'{s/1e9:.2f}G'
        elif s > 1e6:  ps = f'{s/1e6:.2f}M'
        elif s > 1e3:  ps = f'{s/1e3:.2f}K'
        else:          ps = s
        #print(ps, ' '.join(pseudosum[sig]))
        print(ps)
        for x in pseudosum[sig]:
            print("\t", x)

if not 'pseudosum' in globals():
    print(f'No duplicates of file sizes greater than {arg.min} bytes found in "{arg.path}"')


# End timer
t1 = time.time()

if arg.verbose:
    print(f"This run took {t1-t0} seconds.", file = sys.stderr)