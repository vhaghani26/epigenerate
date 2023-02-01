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

python3 duplicate_finder.py --path /share/lasallelab/2018_LaSalle-Yasui_Rodent_Brain_Single_Nuclei_SingleCell/ > /share/lasallelab/Viki/duplicate_files_2018_LaSalle-Yasui_Rodent_Brain_Single_Nuclei_SingleCell.txt

python3 duplicate_finder.py --path /share/lasallelab/Annie/ > /share/lasallelab/Viki/duplicate_files_Annie.txt

python3 duplicate_finder.py --path /share/lasallelab/Antonio/ > /share/lasallelab/Viki/duplicate_files_Antonio.txt

python3 duplicate_finder.py --path /share/lasallelab/Archive/ > /share/lasallelab/Viki/duplicate_files_Archive.txt

python3 duplicate_finder.py --path /share/lasallelab/Ben/ > /share/lasallelab/Viki/duplicate_files_Ben.txt

python3 duplicate_finder.py --path /share/lasallelab/Charles > /share/lasallelab/Viki/duplicate_files_Charles.txt

python3 duplicate_finder.py --path /share/lasallelab/Dag_Yasui/ > /share/lasallelab/Viki/duplicate_files_Dag_Yasui.txt

python3 duplicate_finder.py --path /share/lasallelab/Demario/ > /share/lasallelab/Viki/duplicate_files_Demario.txt

python3 duplicate_finder.py --path /share/lasallelab/Diane/ > /share/lasallelab/Viki/duplicate_files_Diane.txt

python3 duplicate_finder.py --path /share/lasallelab/Florence/ > /share/lasallelab/Viki/duplicate_files_Florence.txt

python3 duplicate_finder.py --path /share/lasallelab/genomes > /share/lasallelab/Viki/duplicate_files_genomes.txt

python3 duplicate_finder.py --path /share/lasallelab/Hyeyeon/ > /share/lasallelab/Viki/duplicate_files_Hyeyeon.txt

python3 duplicate_finder.py --path /share/lasallelab/Jesse/ > /share/lasallelab/Viki/duplicate_files_Jesse.txt

python3 duplicate_finder.py --path /share/lasallelab/Julia/ > /share/lasallelab/Viki/duplicate_files_Julia.txt

python3 duplicate_finder.py --path /share/lasallelab/Kari/ > /share/lasallelab/Viki/duplicate_files_Kari.txt

python3 duplicate_finder.py --path /share/lasallelab/Keith/ > /share/lasallelab/Viki/duplicate_files_Keith.txt

python3 duplicate_finder.py --path /share/lasallelab/perl_lib/ > /share/lasallelab/Viki/duplicate_files_perl_lib.txt

python3 duplicate_finder.py --path /share/lasallelab/programs/ > /share/lasallelab/Viki/duplicate_files_programs.txt

python3 duplicate_finder.py --path /share/lasallelab/pysam/ > /share/lasallelab/Viki/duplicate_files_pysam.txt

python3 duplicate_finder.py --path /share/lasallelab/Rochelle/ > /share/lasallelab/Viki/duplicate_files_Rochelle.txt

python3 duplicate_finder.py --path /share/lasallelab/Theresa/ > /share/lasallelab/Viki/duplicate_files_Theresa.txt

python3 duplicate_finder.py --path /share/lasallelab/Viki > /share/lasallelab/Viki/duplicate_files_Viki.txt

python3 duplicate_finder.py --path /share/lasallelab/Yihui > /share/lasallelab/Viki/duplicate_files_Yihui.txt

# Print out various information about the job
env | grep SLURM                                               # Print out values of the current jobs SLURM environment variables
  
scontrol show job ${SLURM_JOB_ID}                              # Print out final statistics about resource uses before job exits

sstat --format 'JobID,MaxRSS,AveCPU' -P ${SLURM_JOB_ID}.batch

# Note: Run dos2unix {filename} if sbatch DOS line break error occurs