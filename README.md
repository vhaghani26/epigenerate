# Epigenerate

This document is for users in the LaSalle Lab to set up their computer environments on the Genome Center cluster. If you are not familiar with how to use a computing environment, please see [this repository](https://github.com/vhaghani26/python_focus_group) to learn basic UNIX commands and/or Python.

Much of this document was adapted from Dr. Ian Korf's documentation on Spitfire.

## Table of Contents

* [Requesting a Hive Account](#requesting-a-hive-account)
* [Logging into Hive](#logging-into-hive)
* [Requesting an Epigenerate Account](#requesting-an-epigenerate-account)
* [Logging into Epigenerate](#logging-into-epigenerate)
* [Configuring Your Profile](#configuring-your-profile)
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
* [Using R on Epigenerate](#using-R-on-epigenerate)
	* [Loading R](#loading-R)
	* [Installing R Packages](#installing-R-packages)
* [$HOME away from $HOME](#home-away-from-home)
* [Conda Usage](#conda-usage)
* [How the Genome Center Cluster Works (Extra Information)](#how-the-genome-center-cluster-works-extra-information)

## Requesting a Hive Account

We are moving away from Epigenerate in support of a new centralized cluster - Hive. Use these steps to create your account:

1. Go to this webpage: https://hippo.ucdavis.edu/clusters
2. Select "HIVE" for the cluster
3. Select "lasallegrp" as the group
4. Write "Janine LaSalle" for the PI
5. Make your SSH key
	- To make an SSH key, you will need to run the following on a Unix based terminal (which is the native terminal for macOS and Linux, but for Windows may be something like Ubuntu):

```
ssh-keygen
ls -al ~/.ssh
cat ~/.ssh/*.pub
```

6. Copy and paste the ENTIRE key into the prompt 
7. Submit your profile request for approval. Once approved, it may take a few hours for your account to become active

### More on SSH Keys

In order to access your HPC account, you need to generate an SSH key pair for authorization. You generate a pair of keys: a public key and a private key. The private key is kept securely on your computer or device. The public key is submitted to HPCCF to grant you access to a cluster. This helps verify your identity to grant you access to the cluster.

Additional user documentation can be found at https://docs.hpc.ucdavis.edu.

## Logging Into Hive

Your **username** will be emailed to you once your account is live. You will need to log in using the device you generated the SSH key on. Enter your **Kerberos password** when prompted to log in. I will look into how multiple devices work and update this when I figure it out.

### CLI Interface

If you just want to work with the command line, then you can run:

```
ssh {username}@hive.hpc.ucdavis.edu
```

### Desktop Interface

Some software has a Graphical User Interface (GUI), and requires X11 to be enabled. X11 forwarding allows an application on a remote server (in this case, Franklin) to render its GUI on a local system (your computer). How this is enabled depends on the operating system the computer you are using to access Franklin is running.

#### Linux 

If you are SSHing from a Linux distribution, you likely already have an X11 server running locally, and can support forwarding natively. If you are on campus, you can use the `-Y` flag to enable it, like so:

```
ssh -Y {username}@hive.hpc.ucdavis.edu
```

If you are off campus on a slower internet connection, you may get better performance by enabling compression with:

```
ssh -Y -C {username}@hive.hpc.ucdavis.edu
```

If you have multiple SSH key pairs, and you want to use a specific private key to connect to the clusters, use the option `-i` to specify path to the private key with SSH:

```
ssh -i ~/.ssh/id_hpc {username}@hive.hpc.ucdavis.edu
```

#### macOS

macOS does not come with an X11 implementation out of the box. You will first need to install the free, open-source [XQuartz package](https://www.xquartz.org/), after which you can use the same ssh flags as described in the Linux instructions above.

#### Windows

The client you use will determine how you access Hive. If you are using MobaXterm, which is recommended by the Genome Center, X11 forwarding should be enabled by default. You can confirm this by checking that the X11-Forwarding box is ticked under your Franklin session settings. For off-campus access, you may want to tick the Compression box as well.

#### OnDemand

You can alternatively open up an instance of Hive through your browser by logging in here: https://ondemand.hive.hpc.ucdavis.edu. This will allow you to launch an RStudio Server, a Linux Desktop, JupyterLab, or VSCode Server, which are all interactive.

## Requesting an Epigenerate Account

**Note**: If you are new to the lab, please only refer to the instructions about Hive. 

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

## Configuring Your Profile

Whenever you log into a computer, a special file, like `.bashrc` or `.profile` run in the background. These files help you set up how your terminal looks and what commands are available. Most of the time, you will only rely on `.bashrc`, but on the Genome Center HPC, you will actually need a `.profile`. `.bashrc` is a script that runs whenever a new Bash shell is started, whereas `.profile` is sourced by the Bash shell upon login. When logging into Epigenerate, you unknowingly run `.profile`. The complication here is that any process you run outside of that immediate session requires `.bashrc`. This includes things like SLURM, screen, tmux, etc. How do we fix this? Well, we set up our files in a way that you only have to edit one file and they'll both be "in sync." First, we will create our `.profile`:

```
cd ~
touch .profile
```

This creates our `.profile`. I like to put a variety of things in my `.profile`, including aliases and commands to make things easier for myself (but mostly failsafes for when I inevitably do something stupid at the terminal). For example:

```
alias ls="ls -F" # Helps distinguish files, directories, aliases, etc. every time you run ls
alias rm="rm -i" # Makes you confirm deletions before you actually delete something
alias cp="cp -i" # Asks if you want to overwrite an existing file if you're copying a file
alias mv="mv -i" # Asks if you want to overwrite an existing file if you're renaming or moving a file
```

I also like to put some fun personal configuration stuff in there. The following code formats my terminal to make my conda environnment the default text color, my username and hostname green, and my working directory blue. 

```
# Set color codes
GREEN="\[\e[32m\]"
BLUE="\[\e[36m\]"
RESET_COLOR="\[\e[0m\]"

# Customize the PS1 prompt
PS1="${GREEN}\u@\h${RESET_COLOR}: ${BLUE}\W${RESET_COLOR}\$ "
```

For more advanced configuration options, see [here](https://github.com/vhaghani26/epigenerate/blob/main/advanced_configuration.md). Otherwise, once you have determined all the things you want to put in your `.profile`, edit and save it.

Now, you will create a `.bashrc`:

```
cd ~
touch .bashrc
```

All you are going to put in your `.bashrc` is:

```
source ~/.profile
```

To implement any changes, either restart your terminal or run `source ~/.profile` and they will be implemented. 

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

**3. Transfer using Cyberduck**

Cyberduck is a free FTP/SFTP client that can be used to transfer files between Epigenerate and your personal computer. Its user interface looks fairly similar to a Mac finder so it can be helpful to easily navigate through your directories and files. 

1. *First, download Cyberduck (https://cyberduck.io/download/) and open it on your computer*
2. *In the top left corner, click "Open Connection"*
3. *Select “SFTP (SSH File Transfer Protocol)”*
4. *Fill in the server: epigenerate.genomecenter.ucdavis.edu*
5. *Fill in your username and password*
6. *Press connect. Once you've done this once, Cyberduck will remember the Epigenerate server*
7. *Once you're in, you can navigate around directories, download files to your personal computer, and upload files to Epigenerate*
8. *Downloading files from Epigenerate to personal computer (Mac): drag and drop, or click on the file you want to download and go to File --> Download To, or double click on a file and it will download to the most recent location you downloaded to*
9. *Uploading files to Epigenerate: drag and drop*

## Using R on Epigenerate

### Loading R
To see what versions of R are available, run:
```
module avail R
```
To load (a certain version of) R, run:
```
module load R/4.1.0
```
```
R
```
This example loads R v4.1.0, but you can load any available version of R. You should now see the '<' symbol 

### Installing R Packages
To install an R package into a certain directory (e.g. /share/lasallelab/programs...), you must set your R_LIBS_USER variable to that directory before you run R. When you're logged into Epigenerate in your terminal, type:
```
nano ~/.Renviron
```
This will bring you to your .Renviron file. Add a line of text that reads
```
R_LIBS_USER = /share/lasallelab/directory_you_want_packages_to_go_into
````
Save the .Renviron file and then load R as explained above. You can now install your packages. If installation is unsuccessful, email hpc-help@ucdavis.edu

## $HOME away from $HOME 

The authentication system may drop the connection to your home directory after a long time. This means the programs that are running for hours will suddenly lose their connection to your `$HOME` directory. This could very well break whatever you're trying to do. Fortunately, `/share/lasallelab` does not have this problem. The workaround is to reset your `$HOME` to `/share/lasallelab/$USER` and then place all of your configurations in there. To do so, run:

```
export LASALLEHOME=/share/lasallelab/{your_directory}
```

Hopefully the sysadmins fix this someday.

## Conda Usage 

Are you using Conda? The answer should be _yes_. Please see the `conda.md` file for more information.

Assuming you are already using conda, there are a number of environments you can use within the LaSalle Lab group. 

### Comethyl

```
conda activate /quobyte/lasallegrp/programs/.conda/Comethyl_v1.3.0/
```

There are also updates underway to fix the gene annotation:

```
conda activate /quobyte/lasallegrp/programs/.conda/envs/Comethyl_v1.3.0_UPDATED
```

### DMRichR

```
conda activate /quobyte/lasallegrp/programs/.conda/DMRichR_R4.2/
```

### NGS_Tools

This environment is a sort of "base" environment for the lab. It's a catch all for software that is used across many pipelines or needed for quick use (e.g. samtools). While most of the software can be accessed using:

```
conda activate /quobyte/lasallegrp/programs/.conda/NGS_Tools/
```

There are some tools with executable files that need to be hard coded into your `.profile`. Please add the following to your `.profile` if you plan to use any of the following software. Also make sure that the `NGS_Tools` conda environment is activated when running the following.

#### NanoMethPhase

```
# NanoMethPhase
export PATH="$PATH:/quobyte/lasallegrp/programs/.conda/NanoMethPhase"
alias nanomethphase='python /quobyte/lasallegrp/programs/.conda/NanoMethPhase/nanomethphase/__main__.py'
```

Confirm you can run it by running:

```
nanomethphase --help
```

#### DeepMod

```
# DeepMod
export PATH="$PATH:/quobyte/lasallegrp/programs/.conda/DeepMod/bin"
```

Confirm you can run it by running:

```
DeepMod --help
```

Note that the documentation tells you to run:

```
python bin/DeepMod.py [arguments]
```

But I installed and set it up so that you just need to use `DeepMod` instead of `python bin/DeepMod.py`.

#### DeepMod2

```
# DeepMod2
export PATH="$PATH:/quobyte/lasallegrp/programs/.conda/DeepMod2"
```

Confirm you can run it by running:

```
DeepMod2 --help
```

Note that the documentation tells you to run:

```
python DeepMod2/deepmod2 [arguments]
```

But I installed and set it up so that you just need to use `DeepMod2` instead of `python DeepMod2/deepmod2`.

#### Modkit

```
# Modkit
export PATH="$PATH:/quobyte/lasallegrp/programs/.conda/dist_modkit_v0.4.2_10d99bc"
```

Confirm that you can run it by running:

```
modkit --help
```

## How the Genome Center Cluster Works (Extra Information)

The Genome Center cluster is composed of _head_ nodes that submit jobs, _cluster_ nodes that work on jobs, and _file servers_ that store all of the data.

![Cluster Topology](https://github.com/KorfLab/spitfire/blob/main/cluster.png)

While epigenerate can submit jobs to the cluster nodes, most of the time we use it as a loosely managed compute node. What exactly does _loosely_ mean? We don't need to submit jobs via `slurm`. Instead, we run jobs directly via the shell. There is 1 main advantage: jobs start immediately. There is also 1 main problem: other people are also using the computer. As a result, sharing must be cooperative. There are no hard rules, but rather social guidelines.
