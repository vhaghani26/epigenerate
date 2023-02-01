#!/bin/bash
#
#SBATCH --mail-user=vhaghani@ucdavis.edu                       # User email to receive updates
#SBATCH --mail-type=ALL                                        # Get an email when the job begins, ends, or if it fails
#SBATCH -p production                                          # Partition, or queue, to assign to
#SBATCH -J duplicate_finder                                    # Name for job
#SBATCH -o duplicate_finder.j%j.out                            # File to write STDOUT to
#SBATCH -e duplicate_finder.j%j.err                            # File to write error output to
#SBATCH -N 1                                                   # Number of nodes/computers
#SBATCH -n 1                                                   # Number of cores
#SBATCH -c 8                                                   # Eight cores per task
#SBATCH -t 80:00:00                                            # Ask for no more than 80 hours
#SBATCH --mem=16gb                                             # Ask for no more than 16 GB of memory
#SBATCH --chdir=/share/lasallelab/                             # Directory I want the job to run in

# Run aklog to deal with SLURM bug
aklog

# Fail on weird errors
set -o nounset
set -o errexit
set -x

# Run the duplicate finder
python3 duplicate_finder.py --path /share/lasallelab/Aron/ > /share/lasallelab/Viki/duplicate_files_Aron.txt

python3 duplicate_finder.py --path /share/lasallelab/Jules/ > /share/lasallelab/Viki/duplicate_files_Jules.txt

python3 duplicate_finder.py --path /share/lasallelab/Logan/ > /share/lasallelab/Viki/duplicate_files_Logan.txt

python3 duplicate_finder.py --path /share/lasallelab/Oran/ > /share/lasallelab/Viki/duplicate_files_Oran.txt

python3 duplicate_finder.py --path /share/lasallelab/Osman/ > /share/lasallelab/Viki/duplicate_files_Osman.txt

python3 duplicate_finder.py --path /share/lasallelab/Kelly/ > /share/lasallelab/Viki/duplicate_files_Kelly.txt

# Print out various information about the job
env | grep SLURM                                               # Print out values of the current jobs SLURM environment variables
  
scontrol show job ${SLURM_JOB_ID}                              # Print out final statistics about resource uses before job exits

sstat --format 'JobID,MaxRSS,AveCPU' -P ${SLURM_JOB_ID}.batch

# Note: Run dos2unix {filename} if sbatch DOS line break error occurs