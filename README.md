# Epigenerate

This document is for users in the LaSalle Lab to set up their computer environments on the Genome Center cluster. If you are not familiar with how to use a computing environment, please see [this repository](https://github.com/vhaghani26/python_focus_group) to learn basic UNIX commands and/or Python.

Much of this document was adapted from Dr. Ian Korf's documentation on Spitfire.

## Table of Contents

* [Requesting an Epigenerate Account](#requesting-an-epigenerate-account)
* [Logging into Epigenerate](#logging-into-epigenerate)
* [Best Practices](#best-practices)
    * [Epigenerate Slack Channel](#epigenerate-slack-channel)
	* [RAM](#ram)
	* [CPUs](#cpus)
* [Data Storage](#data-storage)
	* [On Epigenerate](#on-epigenerate)
	* [The L-Drive](#the_l-drive)
	* [Duplicated Data](#duplicated-data)
	* [Aliasing Data](#aliasing-data)
	* [Transferring Data](#transferring-data)
* [$HOME away from $HOME](#$home-away-from-$home)
* [Conda Usage](#conda-usage)
* [How the Genome Center Cluster Works (Extra Information)](#how-the-genome-center-cluster-works-(extra-information))


## Requesting an Epigenerate Account 

You'll need an account to connect to epigenerate and the rest of the cluster. Use these steps to request an account:

1. Go to this webpage: https://computing.genomecenter.ucdavis.edu
2. Follow the "request account" link
3. Select Janine LaSalle from the list of sponsors
4. You will get an email with a link where you can set your password

For help, email hpc-help@ucdavis.edu.

## Logging into Epigenerate 

To log in to epigenerate, use `ssh`. In the following example, the user's name is `username`. Switch this to whatever user name you have.

```
ssh username@epigenerate.genomecenter.ucdavis.edu
```

This will prompt you to enter your password. If you are new to the command line, it is important to note that you will not see any characters appear as you type your password. Just type your password and click "Enter" and you will be logged in.

## Best Practices 

### Epigenerate Slack Channel

On the LaSalle Lab Slack, you should locate a channel called "epigenerate." If you plan to use epigenerate at all, please join this Slack channel. This is where discussions regarding resource intensive jobs will take place. There will also be general updates regarding storage expansions, increases in RAM, cluster outages, etc., so be sure to join it!

### RAM 

RAM is the hardest resource to share. A good rule of thumb is for each user to never use more than half of the total RAM. Since there is currently 500G RAM, never run jobs that take more than 250G in total. So don't set up 50 jobs, each taking 10G RAM. If you have no idea how much RAM your process is using, run `top` or `htop` and examine the memory usage. You can also run these commands to check active usage before you try running a job.

If you know you are going to be running a resource-intensive job, such as Comethyl, then you have some options regarding how to do so.

1. Discuss with the cluster overseer (currently Viki) and other epigenerate users to confirm usage of epigenerate's RAM
2. Cap the memory of the job using `ulimit`. There is more information on what `ulimit` is [here](https://www.geeksforgeeks.org/ulimit-soft-limits-and-hard-limits-in-linux/), but below is an example of how you can implement it:

```
ulimit -v 250000000 # Set RAM/memory limit to 250000000 kb (250 GB)
{the command you are running}
ulimit -v unlimited # Reset your memory cap to being unlimited
```

3. Submit the resource-intensive job via SLURM. See the [SLURM directory](https://github.com/vhaghani26/epigenerate/tree/main/SLURM) for information on how to create and submit a SLURM script.

### CPUs

(Viki needs to check how many CPUs are on epigenerate; this needs to be rewritten)

CPU is easily shared but you should still be cognizant of how much you are using. There are 64 CPUs and you shouldn't use more than half (32) at a time. However, if you have some kind of rush job, you can use most of them if you `nice` your jobs to reduce their priority. In fact, if you want to be a good lab citizen, you will `nice` all of your jobs. To `nice` your job, simply put precede your command with the word `nice`.

## Data Storage

### On Epigenerate 

Most LaSalle lab members and epigenerate users will be using the `/share/lasallelab/` mount point to store code, data, and experiments. This is your main hub on the file system, not your home directory.

* `/share/lasallelab/data` - contains raw data in the format `{year}_{project_or_data_title}`
* `/share/lasallelab/data/genomes` - contains genome files organized by species

To determine how much space you have available, use `df`.

```
cd /share/lasallelab/
df -h .
```

This will report the size of the partition and how much is in use. If you want to know exactly how much is in each project directory (for example), use `du`.

```
du -h -d 1 /share/lasallelab/DirectoryName
```

### The L-Drive 

In order to ensure we have a data back-up and that we do not have duplicate data on Epigenerate, one copy (read-only) or data will be maintained in `/share/lasallelab/data/`, while another will be hosted on the L-drive. The L-drive copy should be untouched aside from download. In order to access the L-drive and find out more about it, please take a look at the [L-Drive](https://github.com/vhaghani26/epigenerate/tree/main/L-Drive) directory.
	
### Duplicated Data 

In the event that the best practices are not followed, we may end up with large levels of duplicated files taking up storage space. As such, there is a program Viki Haghani has written to detect all duplicates and report them back. For more information on how to run it, please head over to the [Duplicate_Finder](https://github.com/vhaghani26/epigenerate/tree/main/Duplicate_Finder) directory.

### Aliasing Data

One way we can prevent duplicated data is by aliasing (linking) the files we need into our own directories.

### Transferring Data 

To copy files to epigenerate, use `scp`.

```
scp my_file username@epigenerate.genomecenter.ucdavis.edu:/share/lasallelab/FileName
```

You can also copy whole directories with the `-r` option.

```
scp -r my_dir username@epigenerate.genomecenter.ucdavis.edu:/share/lasallelab/DirectoryName
```

Of course, you can also `scp` files or directories from epigenerate back to your personal computer.

```
scp -r username@epigenerate.genomecenter.ucdavis.edu:/share/lasallelab/DirectoryName .
```

## $HOME away from $HOME 

The authentication system may drop the connection to your home directory after a long time. This means the programs that are running for hours will suddenly lose their connection to your `$HOME` directory. This could very well break whatever you're trying to do. Fortunately, `/share/lasallelab` does not have this problem. The workaround is to reset your `$HOME` to `/share/lasallelab/$USER` and then place all of your configurations in there. Hopefully the sysadmins fix this someday.

## Conda Usage 

Are you using Conda? The answer should be _yes_. Is the Conda directory in your home directory? The answer should be _no_. Reset your $HOME to `/share/lasallelab/$USER` and do **all** of your work from there. Please see the `conda.md` file for more information.

## How the Genome Center Cluster Works (Extra Information)

The Genome Center cluster is composed of _head_ nodes that submit jobs, _cluster_ nodes that work on jobs, and _file servers_ that store all of the data.

![Cluster Topology](https://github.com/KorfLab/spitfire/blob/main/cluster.png)

While epigenerate can submit jobs to the cluster nodes, most of the time we use it as a loosely managed compute node. What exactly does _loosely_ mean? We don't need to submit jobs via `slurm`. Instead, we run jobs directly via the shell. There is 1 main advantage: jobs start immediately. There is also 1 main problem: other people are also using the computer. As a result, sharing must be cooperative. There are no hard rules, but rather social guidelines.