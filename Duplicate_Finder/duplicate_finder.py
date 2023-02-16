import argparse
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
		mode = os.lstat(filepath).st_mode
		if not stat.S_ISREG(mode): continue
		s = os.path.getsize(filepath)
		if s < arg.min: continue
		if s not in size: size[s] = []
		size[s].append(filepath)

#####################
## Find Duplicates ##
#####################
    
# Find duplicate files (1) by file size (2) by pseudo-checksum
for s in sorted(size, reverse=True):
    if arg.verbose:
        print("Finding duplicate files by filtering for file size...", file = sys.stderr)
    
	if len(size[s]) == 1: continue
    
    if arg.verbose:
        print("Calculating psuedo-checksum for potentially duplicated files...", file = sys.stderr)
    
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
    
    if arg.verbose:
        print("Determining duplicates..", file = sys.stderr)
    
	# Report duplicates
	for sig in pseudosum:
		if len(pseudosum[sig]) == 1: continue
		ps = None
		if   s > 1e12: ps = f'{s/1e12:.2f}T'
		elif s > 1e9:  ps = f'{s/1e9:.2f}G'
		elif s > 1e6:  ps = f'{s/1e6:.2f}M'
		elif s > 1e3:  ps = f'{s/1e3:.2f}K'
		else:          ps = s
		print(ps, ' '.join(pseudosum[sig]))
