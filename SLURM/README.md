# SLURM and the Cluster

This material was adapted from [Dr. C. Titus Brown's material](https://github.com/ngs-docs/2021-GGG298/tree/latest/Week9-Slurm_and_Farm_cluster_for_doing_analysis) and the [UC Davis Bioinformatics Core's SLURM workshop](https://ucdavis-bioinformatics-training.github.io/2023-October-Slurm-Seminar/cluster_training/intro).

## What is a Cluster?

A cluster can be thought of as a group of computers which work together to allow you to perform memory intensive functions. Clusters are accessed by logging onto one computer (**head node**) and resources (other computers) are acquired by asking for resources from job schedulers.

<center><img src="https://i.imgur.com/2nl5zzP.png" width="80%"></a></center>

Image modified from [vrlab](http://www.vrlab.umu.se/documentation/guides/beginner-guide)

## How do Clusters Work?

### Job Schedulers

In order to carry out commands that are memory intensive we need to use auxiliary computers that will not affect the login/head node. **NOTE:** sometimes merely copying large files is memory intensive enough that we will need to use computers other than the head node! To request resources to run our scripts we use _job schedulers_. Job schedulers handle how to allocate the compute cluster's resources to batch job scripts submitted by users.

There are a number of different flavors of job schedulers. The job scheduler you will be submitting jobs to is specific to the cluster you are using at your institution but they all have the following general structure:

![](https://i.imgur.com/9rSbIxR.png)

The job scheduler evaluates when resources will be dedicated to a job based on the:
* Partition & priority (`-p`)
* How much of  the group's resources are already being used
* Requested wall time (`-t`)
* Requested resources
    * memory (`--mem`)
    * CPUs (`-c`)

## SLURM

[**SLURM**](https://slurm.schedmd.com/documentation.html) (**S**imple **L**inux **U**tility for **R**esource **M**anagement) is an open source workload manager that is commonly used on compute clusters (both the FARM and barbera use SLURM). It handles allocating resources requested by batch scripts. 

There are **two** main ways you can request resources using SLURM:

### 1. Run an interactive session with `srun`

Interactive sessions allow you to work on computers that aren't the login/head node. Essentially you can do everything you've done at the command line interface on the cluster. This is really powerful for doing memory intensive commands that you may not need to keep track of. However, with this power comes a great danger. 

*Why is it dangerous?*
The commands you run will not be saved in scripts anywhere. So, if you wanted to go back and recreate an analysis, you won't know what you've run, how you've run it or which versions of software you used.

To request and launch a basic interactive session that will last for two hours use the following:

```
srun --time=02:00:00 --pty /bin/bash
```

Pay close attention to the time you give to yourself using `srun`! SLURM will terminate the session immediately at the end of the allotted time. It, sadly, doesn't care if you are 99.99% of the way through your analysis :(

Also, you can request more/different resources by using to following flags:
* `--mem=<number>Gb` - request a certain amount of memory
* `-c <number>` - request a certain number of CPUs
* `--pty R` - request an interactive R session
* `--account` - specifies the account; either `publicgrp`, which has a high and low partition (with a 3 day job time limit) or `lasallegrp`, which has a high partition and prioritizes our jobs compared to others

Any of the options you add should come before the `--pty` argument. For example, this will **not** work:

```
srun --time=00:05:00 --pty /bin/bash --mem=4Gb --account publicgrp --partition low
```

But this will work:

```
srun --time=00:05:00 --mem=4Gb --account publicgrp --partition low --pty /bin/bash
```

Once you are done your `srun` session, type `exit` so that the resources can be used by someone else since you are no longer using them. This is the nice thing to do!

### 2. Submit batch scripts with `sbatch`

Batch job scripts (also known as job scripts) are scripts that contain `#!/bin/bash` at the beginning of each script and are submitted to the SLURM workload manager by using `sbatch`. They are scripts that contain code usually written in `bash`. We can use most commands (and a few more) that we would use at the command line within our `sbatch` scripts.

When we submit a script to SLURM it is considered a _job_ and gets a unique `job_ID` assigned to it. Jobs can be submitted to SLURM with the `sbatch` command:

```
sbatch {your_script}.slurm
```

In order to handle jobs, SLURM needs to know the maximum amount of **walltime** your job will run. Walltime is literally "the time shown on the clock on the wall." It is the expected amount of time from the start of your code running to when the last command in your script finishes. (Always make this longer than you think you will need, because the cluster will kill your job if it exceeds it! I'm unfortunately speaking from experience here). We can tell SLURM how much time to allow our submitted script by using the `-t` flag. For example, let's tell SLURM that our job _shouldn't_ take longer than 5 minutes (note: the format is `dd-hh:mm:ss`).

```
sbatch -t 00-00:05:00 {your_script}.slurm
``` 

You will see your job was successfully submitted and will be given an associated Job ID number: `Submitted batch job {job_id}`

#### Flags to use when submitting jobs

We can use a number of different flags to specify resources we want from SLURM:
* The **partition** we would like to use for our job––this will also entail the _priority_ in which our job is submitted (priorities can be high, medium or low). We can request a partition by using the following flag: `-p {name_of_partition}`
* The **memory** required to run our job. We can request a specified amount of time with the following flag: `--mem={number}Gb`
* We can have SLURM **mail** us updates about our job, such as when it starts(`BEGIN`), ends(`END`), if it fails(`FAIL`) or all of the above (`ALL`). There are many other mail-type arguments: REQUEUE, ALL, TIME_LIMIT, TIME_LIMIT_90 (reached 90 percent of time limit), TIME_LIMIT_80 (reached 80 percent of time limit), TIME_LIMIT_50 (reached 50 percent of time limit) and ARRAY_TASKS. We can request SLURM emails us with the following flags: `--mail-user={your_email} --mail-type={argument}`
* We can also give jobs specific **names**. To name your job use: `-J {job_name}` Be careful, as there is a limit to the number of characters your job name can be.
* SLURM automatically generates **output scripts** where all of the output from commands run from the script are printed to. These will take the form as `slurm-12345.out` where 12345 is an identifying number (the job ID, by default!) SLURM assigns to the file. We can change this to any output file name we want. To specify the name of your output file use `-o {file_name}.out`
* SLURM can generate **error files**, where all of the errors from the script are printed to. We can ask SLURM to create err files and name them with `-e {file_name}.err`

If we were being mean to ourselves we would write these out at the command line each time we submitted a job to SLURM with `sbatch`. It would look something like this:

```
sbatch --time=01-02:03:04 -p high --mem=4Gb --mail-user={your_email} --mail-type=ALL -J {job_name} -o {file_name}.out -e {file_name}.err
```

Typing all of the parameters out on the command line every time we want to submit a batch script is annoying and it also doesn't allow us to record what parameters we used easily. We can instead put the parameters to run each job in the script we submit to SLURM!
  
#### Repeatability: SLURM Scripts

One of the most important things in science is repeatability. This sentiment holds true in bioinformatics experiments as well. However, it is exceptionally easy to run a series of command on data, leave the data for a few months (or years) and come back to the data and have no clue how you went from point A to point Z. This is not good.

Let's say we lost everything except our backed up raw data and we needed to recreate an analysis. In the worst case, the commands used to carry out the experiment were not saved. We would have to figure out all of the commands with only a vague memory of the steps we took to get results. It is hard, if not impossible to recreate an analysis with exactly the same string of commands and parameters. So, we should think about documenting things as we go.

In the best case (of this terrible scenario) we would have a script to recreate our analysis! So, we can make this easy for our _future_ forgetful-selves and put all of the flags and commands we submit to SLURM INSIDE our batch scripts!

We can do this by adding **#SBATCH** lines of code after the sh-bang line (`#!/bin/bash`) in our script.

Here is a template of a SLURM script.

```
#!/bin/bash
#
#SBATCH --mail-user=vhaghani@ucdavis.edu                            # User email to receive updates
#SBATCH --mail-type=ALL                                             # Get an email when the job begins, ends, or if it fails
#SBATCH -p high		                                                # Partition, or queue, to assign to
#SBATCH -J job_name		                                            # Name for job
#SBATCH -o job_name.j%j.out              		                    # File to write STDOUT to
#SBATCH -e job_name.j%j.err                  		                # File to write error output to
#SBATCH -N 1                                                        # Number of nodes/computers
#SBATCH -n 1                                                        # Number of cores
#SBATCH -c 8                                                        # Eight cores per task
#SBATCH -t 72:00:00                                                 # Ask for no more than 72 hours
#SBATCH --mem=6gb                                                   # Ask for no more than 6 GB of memory
#SBATCH --chdir=/quobyte/lasallegrp/Viki/my_project_directory	    # Directory I want the job to run in

# Source your config file (usually ~/.bashrc or ~/.profile) so conda can be used
source {config_file}


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
```

I have included a template file in this directory so you can copy it to make your own SLURM script. You can download it using:

```
wget https://github.com/vhaghani26/epigenerate/blob/main/SLURM/slurm_template.slurm
```

Side Note: I have [read](https://github.com/dib-lab/farm-notes/blob/latest/advanced-usage.md) that generally, you should use `-N 1` and `-n 1` and only adjust the number of CPUs with `-c` to reflect the number of jobs being submitted. As such, just leave `-N` and `-n` as 1. 

#### Monitor your jobs with `squeue`

Oftentimes we submit jobs and would like to know certain things about them -- if they've started, how long they've been running, if they are _still_ running, etc, etc... We can look at the status of any job SLURM is handling by using `squeue`. This will output a list of **ALL** the jobs currently submitted to SLURM. Often we won't be able to scroll through the list to find our job(s). So, in order to only see your own job(s) we can specify a **username**:

If you don't know your username, you can find it in a couple of ways:

1. the `whoami` command:

```
whoami
```

2. with  $USER

```
echo $USER
```

Note: there are subtle differences between the two. The `whoami` command displays the effective user id at the time the command is entered. The `$USER` is an environment variable that is set by the shell--it won't work on all operating systems, so just be mindful.

We can use the output of this to see the status of the jobs associated with a particular username (yours or another user's can be displayed):

```
squeue -u {username}
```

If you don't care about other people's jobs, you can also just use the `--me` flag instead of `-u {username}` like so:

```
squeue --me
```

We can also expand our view to show the full rule name (the default is 8 characters long, which is too short for my uses at times). It also displays how long a job has been running next to the time limit. As such, I find this more informative than the above command:

```
squeue --format="%.18i %.9P %.30j %.8u %.8T %.10M %.9l %.6D %R" --me
```

#### Cancel your jobs with `scancel`

To cancel a single job you can specify the `JOBID`

```
scancel {job_ID}
```

To cancel all of the jobs that belong to you, use the `-u`flag.

```
scancel -u {username}
```