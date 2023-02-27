# Duplicate Finder

## Running `duplicate_finder.py` 

**Arguments**

* `--path` is a required argument referring to the directory you are testing for duplicates
* `--output` is a required argument referring to the output file containing the results
* `--min` is an optional argument that allows you to specify the minimum file size in bytes to check duplicates for (default is 1024)
* `--bytes` is an optional argument that allows you to specify the minimum number of bytes to calculate a pseudo checksum for (default is 128)

If you are running `duplicate_finder.py` locally or at the command line directly (i.e. not SLURM), you will need to ensure that the paths are correct given the directory you are running it in. I recommend downloading `duplicate_finder.py` to the parent directory of the directory you are testing for duplicates. If you do so, you may run the following:

```
python3 duplicate_finder.py --path {duplicate_containing_directory} --output duplicate_finder_results.txt
```

If you are running `duplicate_finder.py` through SLURM, which is recommended if you are searching through large volumes of files, then create a SLURM script and submit the slurm script. I find that using absolute paths in SLURM scripts prevents erroring out, so be mindful of replacing the paths in the template below with the appropriate ones for your computational environment.

```
#!/bin/bash
#
#SBATCH --mail-user=vhaghani@ucdavis.edu                            # User email to receive updates
#SBATCH --mail-type=ALL                                             # Get an email when the job begins, ends, or if it fails
#SBATCH -p production                                               # Partition, or queue, to assign to
#SBATCH -J duplicate_finder                                         # Name for job
#SBATCH -o duplicate_finder.j%j.out                                 # File to write STDOUT to
#SBATCH -e duplicate_finder.j%j.err                                 # File to write error output to
#SBATCH -N 1                                                        # Number of nodes/computers
#SBATCH -n 1                                                        # Number of cores
#SBATCH -c 8                                                        # Eight cores per task
#SBATCH -t 72:00:00                                                 # Ask for no more than 72 hours
#SBATCH --mem=6gb                                                   # Ask for no more than 6 GB of memory
#SBATCH --chdir=/share/lasallelab/Viki/epigenerate/Duplicate_Finder # Directory I want the job to run in

# Run aklog to deal with SLURM bug
aklog

# Source profile so conda can be used
source /share/korflab/home/viki/profile

# Initialize conda
. /software/anaconda3/4.8.3/lssc0-linux/etc/profile.d/conda.sh

# Activate your desired conda environment
conda activate /share/korflab/home/viki/.conda/dup_find

# Fail on weird errors
set -o nounset
set -o errexit
set -x

# Run the duplicate finder
python3 duplicate_finder.py --path /share/lasallelab/ --output /share/lasallelab/Viki/epigenerate/Duplicate_Finder/2023_02_03_duplicate_files_results.txt

# Print out various information about the job
env | grep SLURM                                               # Print out values of the current jobs SLURM environment variables

scontrol show job ${SLURM_JOB_ID}                              # Print out final statistics about resource uses before job exits

sstat --format 'JobID,MaxRSS,AveCPU' -P ${SLURM_JOB_ID}.batch

# Note: Run dos2unix {filename} if sbatch DOS line break error occurs
```

To submit the script, run

```
sbatch {slurm_script}
```

## Interpreting Outputs

The output of the program will have the file size followed by the locations of duplicate files. For example:

```
1.49K
	/location1/that/contains/duplicates/some_file.txt
	/location2/that/contains/duplicates/some_file_duplicate.txt
```

This is intended for users to easily see where all multiple copies of files are located to ensure that they can be addressed appropriately.

## Verifying Duplicates

If, for some reason, you have believe that two files were incorrectly marked as documents, you can verify using an MD5 checksum. To do so, run the following:

```
md5sum {file}
```

The first column is the hash value output by the checksum and the second is the file name. The probability that the files are identical by chance is 1.47e-29, indicating that they're effectively identical if the output hashes are the same.