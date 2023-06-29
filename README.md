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
	* [The L-Drive](#the-l-drive)
	* [Duplicated Data](#duplicated-data)
	* [Aliasing Data](#aliasing-data)
	* [Transferring Data](#transferring-data)
* [$HOME away from $HOME](#home-away-from-home)
* [Conda Usage](#conda-usage)
* [How the Genome Center Cluster Works (Extra Information)](#how-the-genome-center-cluster-works-extra-information)


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

As a general rule of thumb, if you are running a resource-intensive job that can be run on SLURM, please do so in order to allow others that are running programs that must be run on Epigenerate (e.g. Comethyl) to have access to Epigenerate's resources.

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
4. If you are running a memory intensive job in R on epigenerate such as Comethyl, limit your R environment memory to 250 GB max. Log in to the cluster and run the following code

```
nano ~/.Renviron
```
Paste the following inside the file and save it 
```
R_MAX_VSIZE=250Gb 
```
5. Comethyl uses a lot of resources, but you can reduce the RAM required by changing a couple of default parameters. The two steps that are particularly resource-intensive are
```
getSoftPower
```
and
```
getModules
```
To address this, Comethyl breaks the genome into blocks for analysis for both of these steps. The default block size is 40000, which can be decreased to reduce RAM. To do this, run the functions (available at https://github.com/cemordaunt/comethyl) with your block size of choice for each function (the argument for getSoftPower is called blockSize and for getModules is called maxBlockSize). For example, the first part of each function is shown here, with the block size set to 10000:
```
getSoftPower <- function(meth, powerVector = 1:20,
                         corType = c("pearson", "bicor"), maxPOutliers = 0.1,
                         RsquaredCut = 0.8, blockSize = 10000,
                         gcInterval = blockSize - 1, save = TRUE,
                         file = "Soft_Power.rds", verbose = TRUE)
```
and
```
getModules <- function(meth, power, regions, maxBlockSize = 10000,
                       corType = c("pearson", "bicor"), maxPOutliers = 0.1,
                       deepSplit = 4, minModuleSize = 10, mergeCutHeight = 0.1,
                       nThreads = 4, save = TRUE, file = "Modules.rds",
                       verbose = TRUE)
```
From here, you can run Comethyl as usual and many fewer resources will be used

### CPUs

CPU is easily shared but you should still be cognizant of how much you are using. There are 64 CPUs allocated to epigenerate (you can check CPU number by running `lscpu`). Do not use more than half (32) at a time without consulting other lab members first.

**1. Using `nice`**

Although you should generally limit usage to 32 CPUs, if you have some kind of a rush job, you can use most of them if you `nice` your jobs to reduce their priority. In fact, if you want to be a good lab citizen, you will `nice` all of your jobs. To `nice` your job, simply put precede your command with the word `nice` (e.g. `nice {your_command}`). As a general rule of thumb, `nice` your job if you expect it to run for over 24 hours. If nobody else is using epigenerate at the time, this still gives you the full allocation of resources you are running your program with.

To better understand what it means to `nice` your job, your `nice` value is set to a default of 0 on epigenerate. The more "nice" you are, the higher your `nice` value. The maximum range of `nice` is 19, meaning that you are giving your job the lowest priority. When you run `nice`, it uses a default of `+10` to your `nice` value, effectively taking you from 0 to 10. If you want to make this higher or lower, you can use the `-n` command to specify how "nice" you would like to be. This means, for example, that you could run something like `nice -n 5 {your_command}`, increasing your "niceness" by 5 instead of 10. Essentially, the higher the number, the nicer you are being with resource allocation.

**2. Using `renice`**

Let's say you're running something and it's taking longer than expected. You start to worry and you're not sure when it's going to finish, but you didn't `nice` your job when you started it. Fortunately, you can use `renice` to reassign the `nice` value! To use `renice`, you either need the process ID (which is labeled as `PID` when you run `htop`) or your user ID. 

If you are running with the `PID`, then run the following:

```
renice -n {new_nice_value} -p {PID}
```

Some programs split into many processes, which makes it complicated to track and limit each one. In these cases, it may be easier to use your user ID:

```
renice -n {new_nice_value} -u {username}
```

Be mindful that this affects EVERY job you are actively running. Your `nice` value will not be reset until you close all open terminals in which you are actively logged into epigenerate.


## Data Storage

### On Epigenerate 

Most LaSalle lab members and epigenerate users will be using the `/share/lasallelab/` mount point to store code, data, and experiments. This is your main hub on the file system, not your home directory.

* `/share/lasallelab/data` - contains raw data in the format `{year}_{project_or_data_title}`
* `/share/lasallelab/genomes` - contains genome files organized by species

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

One way we can prevent duplicated data is by aliasing (linking) the files we need into our own directories. Linking files or directories is an extremely powerful tool. Let's say I downloaded and processed the entire human genome as a reference file on epigenerate and now someone else wants to use it. Instead of copying the whole file into their directory to work with, they can create a symbolic link to the file within their own directory. This allows them to use/access the file or directory without taking up any extra space - especially for such a large file! The **l**i**n**k command, `ln`, allows us to do this. Before we get started, there are a few things that may be helpful to explain. First, when we use the command, it will generally look like this:

```
ln -s <original file> <link to file>
```

Second, we will always use the `-s` option when using `ln`. `-s` represents that the link is "symbolic," which means that it creates a soft link rather than a hard link. A **soft link** is equivalent to a shortcut in Windows, or rather a redirection to the original location and file. A **hard link**, on the other hand, associates two files (which may have different names) to the same file information. We don't want hard links; we only want to use soft links, hence our strict use of `ln -s` instead of *just* `ln`.

### Transferring Data 

**1. Transfer using `scp`**

To copy files to epigenerate, you can use `scp`.

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

**2. Transfer using `rsync`**

Alternative transfer protocol from epigenerate to local, use `rsync`. `rsync` is famous for its delta-transfer algorithm, which reduces the amount of data sent over the network by sending only the differences between the source files and the existing files in the destination. Rsync is widely used for backups and mirroring and as an improved copy command for everyday use.

TLDR; it only transfers files that haven't been transfered and does not overwrite or replace already exisiting files.

*Transfer from epigenerate to local*

Perform an `rsync` dry run using `-n`, `-a` archives files, `-z` compresses files, `-P` shows progress, and `-v` is verbose which will tell you how many files and the size of the data being transferred. *ssh to epigenerate is not required, run this on terminal locally*

```
rsync -azPnv username@epigenerate.genomecenter.ucdavis.edu:/share/lasallelab/UserFolder/DirectoryName "local path"
```

The local path is identified by right-clicking your folder and selecting "Copy as Pathname" (PC) or by right clicking your folder and holding the option key (Mac) "Copy 'Folder Name' as Pathname"

Run `rsync` by removing `-nv`

```
rsync -azP username@epigenerate.genomecenter.ucdavis.edu:/share/lasallelab/UserFolder/DirectoryName "local path"
```

If transfer fails, run `rsync` again and the transfer will resume from the last file being transferred

*Transfer from local to epigenerate*

Perform `rsync` dry run to check if file paths are correct. If using an external drive or the L-drive please put path in `""`. `""` is not required for local folders in your personal computer. Example below is for files in external drives. Remove `""` for local folders.

```
rsync -azPnv "local path" username@epigenerate.genomecenter.ucdavis.edu:/share/lasallelab/UserFolder/DirectoryName
```

**Highly recommend running a dry run before every transfer to check files being transferred.**

```
rsync -azP "local path" username@epigenerate.genomecenter.ucdavis.edu:/share/lasallelab/UserFolder/DirectoryName
```

## $HOME away from $HOME 

The authentication system may drop the connection to your home directory after a long time. This means the programs that are running for hours will suddenly lose their connection to your `$HOME` directory. This could very well break whatever you're trying to do. Fortunately, `/share/lasallelab` does not have this problem. The workaround is to reset your `$HOME` to `/share/lasallelab/$USER` and then place all of your configurations in there. To do so, run:

```
export LASALLEHOME=/share/lasallelab/{your_directory}
```

Hopefully the sysadmins fix this someday.

## Conda Usage 

Are you using Conda? The answer should be _yes_. Is the Conda directory in your home directory? The answer should be _no_. Reset your $HOME to `/share/lasallelab/$USER` and do **all** of your work from there. Please see the `conda.md` file for more information.

## How the Genome Center Cluster Works (Extra Information)

The Genome Center cluster is composed of _head_ nodes that submit jobs, _cluster_ nodes that work on jobs, and _file servers_ that store all of the data.

![Cluster Topology](https://github.com/KorfLab/spitfire/blob/main/cluster.png)

While epigenerate can submit jobs to the cluster nodes, most of the time we use it as a loosely managed compute node. What exactly does _loosely_ mean? We don't need to submit jobs via `slurm`. Instead, we run jobs directly via the shell. There is 1 main advantage: jobs start immediately. There is also 1 main problem: other people are also using the computer. As a result, sharing must be cooperative. There are no hard rules, but rather social guidelines.
