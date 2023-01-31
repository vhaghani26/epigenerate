import argparse
import os

# Initialize argparse
parser = argparse.ArgumentParser(
	description='Find duplicated files within the specified directory')

# Required arguments
parser.add_argument('--path', required=True, type=str,
    metavar='<str>', help='Path to directory')

# Finalization of argparse
arg = parser.parse_args()

# Get the path p, sub_directory sub_dir, and filename files from the given path
walk_method = os.walk(arg.path)
 
# Use exception handling to remove the stop iteration from generator object that we get the output from os.walk() method
while True:
    try:
        p, sub_dir, files = next(walk_method)
        break
    except:
        break 

# Create a list of files in directory along with the size
size_of_file = [
    (f,os.stat(os.path.join(arg.path, f)).st_size)
    for f in files
]
  
# Get the size of the sub_dir of the given path
for sub in sub_dir:
    i = os.path.join(arg.path,sub)
    size = 0
    for k in os.listdir(i):
        size += os.stat(os.path.join(i,k)).st_size
    size_of_file.append((sub,size))

# Iterate over list of files along with size 
# Sort by sample size and print
for f, s in sorted(size_of_file,key = lambda x : x[1]):
    print(f'{os.path.join(arg.path, f)}', s)
    #print("{}\t{}MB".format(os.path.join(arg.path,f),round(s/(1024*1024),3)))