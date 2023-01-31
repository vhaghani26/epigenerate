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

# Report file sizes and names
os.system(f'for FILENAME in `find {arg.path}`; do echo -n "$FILENAME "; stat -c "%s" $FILENAME; done')