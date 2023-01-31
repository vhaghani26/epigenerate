import argparse
import os
import subprocess

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

######################
## Compute Checksum ##
######################

# Run checksum only for potentially duplicated files
for key, value in files_and_sizes.items():
    if value in dups and value > arg.bytes:
        # Run and capture checksum
        checksum_byte = subprocess.check_output(['md5sum', f'{key}'])
        # Convert type from byte to string
        checksum_str = checksum_byte.decode('utf-8')
        # Save checksum
        checksum = checksum_str.split(' ')  
        files_and_sizes[key] = [value, checksum[0]]
    else :
        files_and_sizes[key] = [value, "NA"]

# Clear space/memory
del dups

#######################
## Report Duplicates ##
#######################

# Determine duplicate checksums
checksum_list = []
for key, value in files_and_sizes.items():
    if value[1] != "NA":
        checksum_list.append(value[1])

dups = list({x for x in checksum_list if checksum_list.count(x) > 1})

# Clear space/memory
del checksum_list

for key, value in files_and_sizes.items():
    if value[1] in dups:
        print(value[1], key)