#!/usr/bin/env python3

import argparse
import time
import os
import sys
import magic
import subprocess
from collections import defaultdict

# Initiate timer
t0 = time.time()

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
parser.add_argument('--bytes', required=False, default = 0, type=int,
    metavar='<int>', help='Integer describing minimum number of bytes to filter')

# Finalization of argparse
arg = parser.parse_args()

#####################
## Find Duplicates ##
#####################

# Create dictionary for files and file sizes
files_and_sizes = {}

# Populate dictionary
for path, subdirs, files in os.walk(arg.path):
    for name in files:
        files_and_sizes[os.path.join(path, name)] = os.path.getsize(os.path.join(path, name))

# Make a list containing only file sizes
size_list = []
for size in files_and_sizes.values():
    size_list.append(size)

# Find duplicate file sizes
dups = list({x for x in size_list if size_list.count(x) > 1})

# Clear space/memory
del size_list

# Exit program with report that no duplicates were found (proceeds if duplicates found)
if len(dups) < 1:
    print(f"No duplicates found in {arg.path}")
    sys.exit()
    
# Check file type extension and remove aliases
aliases = []
for key, value in files_and_sizes.items():
    ext = f'{magic.from_file(key)}'
    if ext.startswith("symbolic"):
        aliases.append(key)

for alias in aliases:
    if len(aliases) > 0:
        del files_and_sizes[alias]      

# Clear space/memory
del aliases

######################
## Compute Checksum ##
######################

# Run checksum only for potentially duplicated files
for key, value in files_and_sizes.items():
    if value in dups and value > arg.bytes:
        # Run and capture checksum
        ps = subprocess.Popen(('head', '-1000'), stdout = subprocess.PIPE)
        checksum_byte = subprocess.check_output(['md5sum', f'{key}'], stdin = ps.stdout)
        # Convert type from byte to string
        checksum_str = checksum_byte.decode('utf-8')
        # Save checksum
        checksum = checksum_str.split(' ')  
        files_and_sizes[key] = [value, checksum[0]]
    else :
        files_and_sizes[key] = [value, "NA"]

# Clear space/memory
del dups

#########################
## Validate Duplicates ##
#########################

duplicate_files = {}
for pair in files_and_sizes.items():
    if pair[1][1] != "NA":
        if pair[1][1] not in duplicate_files.keys():
            duplicate_files[pair[1][1]] = []
        duplicate_files[pair[1][1]].append(pair[0])
        
# Remove files with same sizes but different checksums
buggy_items = []
for key, value in duplicate_files.items():
    if len(duplicate_files[key]) <= 1:
        buggy_items.append(key)

for bug in buggy_items:
    del duplicate_files[bug]

#######################
## Report Duplicates ##
####################### 

if len(duplicate_files) > 0:
    for key, value in duplicate_files.items():
        print(key)
        for val in value:
            print("\t", val)
else:
    print(f"No duplicates found in {arg.path}")

# Stop timer    
t1 = time.time()
print(f'This run took {t1 - t0} seconds')