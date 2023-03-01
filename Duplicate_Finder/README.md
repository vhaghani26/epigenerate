# Duplicate Finder

## Software Dependencies

There are a few packages required in order to run the duplicate finder. All the dependencies have been packaged in `dup_finder_dependencies.yml`. In order to replicate this environment, make sure that you have conda installed. Download the `yml` file and run the following command in the directory containing the `yml` file.

```
conda env create -n dup_find -f dup_finder_dependencies.yml
```

If you are running the duplicate finder locally, then activate the environment:

```
conda activate dup_find
```

If you are planning to run the duplicate finder using a SLURM script, then you will need to run the conda activation command in the slurm script using the full environment path, which can be identified by running `conda env list`. For example:

```
conda activate /share/korflab/home/viki/.conda/dup_find
```

This will ensure that all software dependencies are met, preventing the program from erroring out.

## Running `duplicate_finder.py` 

**Arguments**

* `--path` is a required argument referring to the directory you are testing for duplicates
* `--bytes` is an optional argument that allows you to specify the minimum file size you are interested in filtering for

If you are running `duplicate_finder.py` locally or at the command line directly (i.e. not SLURM), you will need to ensure that the paths are correct given the directory you are running it in. I recommend downloading `duplicate_finder.py` to the parent directory of the directory you are testing for duplicates. If you do so, you may run the following:

```
python3 duplicate_finder.py --path {duplicate_containing_directory}
```

This will print out the results at the command line. To receive results in a file, run the following:

```
python3 duplicate_finder.py --path {duplicate_containing_directory} > duplicate_finder_results.txt
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
python3 duplicate_finder.py --path /share/lasallelab/ > /share/lasallelab/Viki/epigenerate/Duplicate_Finder/2023_02_03_duplicate_files_results.txt

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

The output of the program will have the unique file ID (checksum) of the first 1000 lines of the file followed by the locations of duplicate files. For example:

```
80256bd7a55509665c4179fd61516745
	/location1/that/contains/duplicates/some_file.txt
	/location2/that/contains/duplicates/some_file_duplicate.txt
```

This is intended for users to easily see where all multiple copies of files are located to ensure that they can be addressed appropriately.

## Verifying Duplicate Directories

When linking full directories, verify that both the directory size AND number of files within the directory are equivalent.

**1. Check Directory Size**

In order to check directory sizes, run the following on both directories of interest.

```
du -sh {directory}
```

If the sizes are different, then they are not identical. If they are identical, proceed to verify that number of contents within the directory.

**2. Check Directory Contents**

Run the following on both directories:

```
ls -1 {directory} | wc -l
```

This will tell you the number of files within the directory. Assuming both the directory size and contents are equivalent, then it is relatively safe to assume that the directories are duplicates. At this point, you remove one of the directories and link the remaining directory in the location of the deleted one.