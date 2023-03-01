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
python3 duplicate_finder.py --path /share/lasallelab/ > /share/lasallelab/Viki/epigenerate/Duplicate_Finder/2023_02_09_duplicate_files_results.txt

# Print out various information about the job
env | grep SLURM                                               # Print out values of the current jobs SLURM environment variables

scontrol show job ${SLURM_JOB_ID}                              # Print out final statistics about resource uses before job exits

sstat --format 'JobID,MaxRSS,AveCPU' -P ${SLURM_JOB_ID}.batch

# Note: Run dos2unix {filename} if sbatch DOS line break error occurs
