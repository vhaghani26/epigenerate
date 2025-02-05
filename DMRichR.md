# Using DMRichR on Epigenerate

## Why is DMRichR a Conda environment now?

The new system set up for the Genome Center HPC does not have modules any more. Essentially, because we are no longer able to module load R and HOMER, I have created a Conda environment for DMRichR. The environment has the most up-to-date version of DMRichR, which uses R 4.2 and Bioconductor 3.16. This also has all the software in one centralized location for everyone to use.

## How to Use DMRichR

In addition to not being able to module load software, we are also moving away from running things directly on head nodes. This means we are going to be switching over to SLURM submissions for our jobs. Here are some instructions regarding how you can submit a DMRichR job:

1. Create your `sample_info.xlsx` file and put it in the same directory as your cytosine reports. Please refer to the DMRichR documentation on [creating your design matrix](https://www.benlaufer.com/DMRichR/articles/DMRichR.html#the-design-matrix-and-covariates). Note that because it's in `xlsx` format, it may be easier to create it on your local machine and `scp` or `rsync` it into the directory on Epigenerate.

2. Navigate to your directory

```
cd /quobyte/lasallegrp/{your_name}/{your_project}/{your_cytosine_reports}
```

3. Create a slurm file

```
nano {project_name}_dmrichr.slurm
```

4. Add the job details to your slurm file and save the file. Here is a SLURM script template for you to use that allows for the usage of the DMRichR environment. Make sure to make the following changes:

* Change `{your_email}` to your email
* Change `{your_cytosine_reports}` to the absolute path (i.e. starting with /quobyte/lasallegrp/...) containing your cytosine reports
* Change `source ~/.profile` if you use a different configuration file (if you set up Conda with Viki, you use .profile)
* Change any desired parameters in the DM.R section of the script

```
#!/bin/bash
#
#SBATCH --job-name=dmrichr             	# Job name
#SBATCH --mail-user={your_email}       	# Your email
#SBATCH --ntasks=70                     # Number of cores/threads
#SBATCH --mem=700000                    # Ram in Mb
#SBATCH --partition=production          # Partition, or queue, to assign to
#SBATCH --time=5-00:00:00              	# Time requested for job
#SBATCH --mail-type=ALL                	# Get an email when the job begins, ends, or fails
#SBATCH --chdir={your_cytosine_reports}	# Your working directory

###################
# Run Information #
###################

start=`date +%s`

hostname

THREADS=${SLURM_NTASKS}
MEM=$(expr ${SLURM_MEM_PER_CPU} / 1024)

echo "Allocated threads: " $THREADS
echo "Allocated memory: " $MEM

####################
# Load Environment #
####################

# Activate the conda environment
conda activate /quobyte/lasallegrp/programs/.conda/envs/DMRichR_R4.2

########
# DM.R #
########

# Run with defaults

call="Rscript \
--vanilla \
/quobyte/lasallegrp/programs/DMRichR/DM_R4.2.R \
--genome mm10 \
--coverage 1 \
--perGroup '0.50' \
--minCpGs 5 \
--maxPerms 10 \
--maxBlockPerms 10 \
--cutoff '0.05' \
--testCovariate Group \
--adjustCovariate Sex \
--sexCheck TRUE \
--GOfuncR TRUE \
--EnsDb FALSE \
--cellComposition FALSE \
--cores 20"

echo $call
eval $call

###################
# Run Information #
###################

end=`date +%s`
runtime=$((end-start))
echo $runtime
```

5. Submit the job

```
sbatch {project_name}_dmrichr.slurm
```

6. Depending on how the SLURM script was edited, there may be an error that says something about "DOS line break error." If this occurs, run:

```
dos2unix {project_name}_dmrichr.slurm
```

And then resubmit the script. You will receive email notifications when your job starts and ends and if it fails!

