import argparse
from subprocess import run
import pandas as pd

# Initialize argparse
parser = argparse.ArgumentParser(
	description='Find duplicated files within the specified directory')

# Required arguments
parser.add_argument('--path', required=True, type=str,
    metavar='<str>', help='Path to directory')

# Finalization of argparse
arg = parser.parse_args()

# Generate output containing file path and file size
cmd = f'for FILENAME in `find {arg.path}`; do echo -n "$FILENAME "; stat -c "%s" $FILENAME; done'
data = run(cmd, capture_output = True, shell = True)
output = data.stdout.splitlines()
errors = data.stderr.splitlines()

# Create data frame
df = pd.DataFrame(output, columns = ['temp'])
df[['file_name','file_size']] = df['temp'].str.split('',expand=True)



print(df)