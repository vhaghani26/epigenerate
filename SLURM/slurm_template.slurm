#!/bin/bash
#
#SBATCH --mail-user={your_email}                                    # User email to receive updates
#SBATCH --mail-type=ALL                                             # Get an email when the job begins, ends, or if it fails
#SBATCH -p production                                               # Partition, or queue, to assign to
#SBATCH -J {job_name}                                               # Name for job
#SBATCH -o {job_name}.j%j.out                                       # File to write STDOUT to
#SBATCH -e {job_name}.j%j.err                                       # File to write error output to
#SBATCH -N 1                                                        # Number of nodes/computers
#SBATCH -n 1                                                        # Number of cores
#SBATCH -c 8                                                        # Eight cores per task
#SBATCH -t 02:00:00                                                 # Ask for no more than 2 hours
#SBATCH --mem=10gb                                                   # Ask for no more than 10 GB of memory
#SBATCH --chdir={your_directory}                                    # Directory I want the job to run in

# Run aklog to deal with SLURM bug
aklog

# Source your config file (usually ~/.bashrc or ~/.profile) so conda can be used
source {config_file}

# Initialize conda (note that the path may differ for you)
. /software/anaconda3/4.8.3/lssc0-linux/etc/profile.d/conda.sh

# Activate your desired conda environment
conda activate {full_env_path}

# Fail on weird errors
set -o nounset
set -o errexit
set -x

# Run your commands
{your_commands_go_here}

# Print out various information about the job
env | grep SLURM                                               # Print out values of the current jobs SLURM environment variables

scontrol show job ${SLURM_JOB_ID}                              # Print out final statistics about resource uses before job exits

sstat --format 'JobID,MaxRSS,AveCPU' -P ${SLURM_JOB_ID}.batch

# Note: Run dos2unix {filename} if sbatch DOS line break error occurs
