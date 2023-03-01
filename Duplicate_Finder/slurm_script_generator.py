#!/usr/bin/env python3

import textwrap
import os

#######################
## Modular Variables ##
#######################

# Date
date1 = "2023_02_01"

# Parent directory (shared lab space)
parent_dir = "/share/lasallelab/"

# Personal directories within the shared space
sub_dirs = [
"2018_LaSalle-Yasui_Rodent_Brain_Single_Nuclei_SingleCell/", 
"Annie/", 
"Antonio/",
"Archive/",
"Aron/",
"Ben/",
"Charles/",
"Dag_Yasui/",
"Demario/",
"Diane/",
"Florence/",
"genomes/",
"Hyeyeon/",
"Jesse/",
"Jules/",
"Julia/",
"Kari/",
"Keith/",
"Kelly/",
"Logan/",
"Oran/",
"Osman/",
"perl_lib/",
"programs/",
"pysam/",
"Rochelle/",
"Theresa/",
"Viki/",
"Yihui/"]

###########################
## Slurm Script Creation ##
###########################

print("Copy the following commands in your terminal to submit the sbatch jobs:")

# Create SLURM files for submission
for sub_dir in sub_dirs:
    slurm_file_info = textwrap.dedent(f"""
    #!/bin/bash
    #
    #SBATCH --mail-user=vhaghani@ucdavis.edu                            # User email to receive updates
    #SBATCH --mail-type=ALL                                             # Get an email when the job begins, ends, or if it fails
    #SBATCH -p production                                               # Partition, or queue, to assign to
    #SBATCH -J duplicate_finder_{sub_dir[:-1]}                           # Name for job
    #SBATCH -o duplicate_finder_{sub_dir[:-1]}.j%j.out                   # File to write STDOUT to
    #SBATCH -e duplicate_finder_{sub_dir[:-1]}.j%j.err                   # File to write error output to
    #SBATCH -N 1                                                        # Number of nodes/computers
    #SBATCH -n 1                                                        # Number of cores
    #SBATCH -c 8                                                        # Eight cores per task
    #SBATCH -t 10:00:00                                                 # Ask for no more than 10 hours
    #SBATCH --mem=5gb                                                   # Ask for no more than 5 GB of memory
    #SBATCH --chdir=/share/lasallelab/Viki/epigenerate/Duplicate_Finder # Directory I want the job to run in
    
    # Run aklog to deal with SLURM bug
    aklog
    
    # Fail on weird errors
    set -o nounset
    set -o errexit
    set -x
    
    # Run the duplicate finder
    python3 duplicate_finder.py --path {parent_dir}{sub_dir} > {parent_dir}Viki/epigenerate/Duplicate_Finder/dup_file_reports/{date1}_duplicate_files_{sub_dir[:-1]}.txt
    
    # Print out various information about the job
    env | grep SLURM                                               # Print out values of the current jobs SLURM environment variables
    
    scontrol show job ${{SLURM_JOB_ID}}                              # Print out final statistics about resource uses before job exits
    
    sstat --format 'JobID,MaxRSS,AveCPU' -P ${{SLURM_JOB_ID}}.batch
    
    # Note: Run dos2unix {{filename}} if sbatch DOS line break error occurs
    """)
    
    # Write file 
    os.system(f'touch {parent_dir}Viki/epigenerate/Duplicate_Finder/slurm_scripts/{date1}_dup_finder_slurm_{sub_dir[:-1]}.slurm')
    with open(f'{parent_dir}Viki/epigenerate/Duplicate_Finder/slurm_scripts/{date1}_dup_finder_slurm_{sub_dir[:-1]}.slurm', 'w') as f:
        f.write(f'{slurm_file_info}')
    os.system(f'sed -i \'1d\' {parent_dir}Viki/epigenerate/Duplicate_Finder/slurm_scripts/{date1}_dup_finder_slurm_{sub_dir[:-1]}.slurm')
    print(f'sbatch {parent_dir}Viki/epigenerate/Duplicate_Finder/slurm_scripts/{date1}_dup_finder_slurm_{sub_dir[:-1]}.slurm')