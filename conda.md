# Conda

Much of this has been adapted from Dr. C. Titus Brown's material teaching Conda and Dr. Ian Korf's Conda setup.

## Why should you use Conda?

Software installation is difficult. It's a confusing ecosystem of operating systems (Mac OS X, many versions of Linux, Windows), and many software has many dependencies (e.g. just consider base language -- C++, Java, Python, R, and their different versions).


![isolation](https://github.com/ngs-docs/2021-GGG298/raw/latest/Week3-conda_for_software_installation/conda-isolation.png)


This leads to confusing situations where different versions of underlying software are needed to run two different programs. What if you wanted to run Macs14 and sourmash both, but one wanted 'python' to mean python2 and the other wanted 'python' to mean python3?

![versions](https://github.com/ngs-docs/2021-GGG298/raw/latest/Week3-conda_for_software_installation/versions.png)

Decoupling user-focused software from underlying operating systems is a Big Deal - imagine, otherwise you'd have to rebuild software for every OS! (This is kind of what conda does for you, actually - it's just centralized!)

Also, lot of software installation currently requires (or at least is much easier with) sysadmin privileges, which is inherently dangerous.

**Why do you need isolated software install environments? Some specific reasons:**

* Your work relies on a bunch of specific versions (perhaps old versions?)
* Working with a collaborator who really likes a particular feature!
* Experiment with new packages without messing up current workflow (reproducibility!)
* Publication ("here's what I used for software", repeatability!)
* Sometimes workflows rely on incompatible software packages! see [Titus' Twitter question](https://twitter.com/ctitusbrown/status/1218252506335080449)

Conda tries to solve all of these problems, and (in my experience) largely succeeds. That's what we'll explore today.

Conda is a solution that seems to work pretty well, and can be used by any user. Downsides are that it can get big to have everyone install their own software system, but it's not that big... (The farm admins like it, too!)

![conda image](https://angus.readthedocs.io/en/2019/_static/conda2.png)

Note that conda emerged from the Python world but is now much broader and works for many more software packages, including R!

## Setting Up Conda Locally

Go to the [Anaconda website](https://www.anaconda.com/download#downloads) and download whatever version is appropriate for your computer setup. Since I use Ubuntu via WSL2 (even though I'm on Windows), I download the Linux version. Once you have downloaded it, change into the directory containing the file and run it. The example below uses my personal setup:

```
cd /mnt/c/Users/vicky/Downloads/
sh Anaconda3-2023.03-1-Linux-x86_64.sh
```

Read the license agreement and answer "yes" (without quotes) to accept the terms. Use the default location for the install by pressing Enter. It will take a little time to install. When the installer asks if you want to initialize Anaconda3 by running conda init, answer "yes."

Close your terminal and open a new one. You should see `(base)` at the start of each prompt. This means you're in the `base` Conda environment. When you install new bioinformatics programs or even programming languages, use Conda to do that for you.

## Setting Up Conda on Epigenerate

As mentioned in the epigenerate documentation, you should be using conda. The problem with conda on epigenerate is that it mounts in your home directory, not in `/share/lasallelab/`. This creates many problems. Here, I will break down some background about conda as well as how you should set it up and use it.

Since Conda does NOT like to be in your home environment, we have to tell it where to go. In the following code, please make sure to replace the appropriate variables, represented within curly brackets `{}`, with your information. 

```
# Paths for conda and software configuration
export LASALLEHOME=/share/lasallelab/{your_directory}
export PATH=$PATH:$LASALLEHOME/bin
export PATH=$PATH:/home/{your_username}/.conda/envs
export PATH=$PATH:/software/anaconda3/4.8.3/lssc0-linux/envs
export CONDA_ENVS_PATH=/share/lasallelab/programs/.conda
export CONDA_PKGS_DIRS=$CONDA_ENVS_PATH/pkgs

# Aliases to improve CLI usage experience
alias ls="ls -F"
alias rm="rm -i"
alias cp="cp -i"
alias mv="mv -i"

# Reconfigure command line display
PS1='\u@\h: \W:\$ '

# Execute conda setup 
__conda_setup="$('/software/anaconda3/4.8.3/lssc0-linux/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
        eval "$__conda_setup"
else
        if [ -f "/software/anaconda3/4.8.3/lssc0-linux/etc/profile.d/conda.sh" ]; then
                . "/software/anaconda3/4.8.3/lssc0-linux/etc/profile.d/conda.sh"
        else
                export PATH="/software/anaconda3/4.8.3/lssc0-linux/bin:$PATH"
        fi
fi
unset __conda_setup
```


Once done, copy the code into your `.bashrc` or `.profile` (or whatever other configuration file you use on epigenerate). This file will be found in your home directory. 

## Using Conda

Now that you have it set up (hopefully) properly, we need to initialize it. Run the following, and change `.bashrc`, if needed, to whatever configuration file you use.

```
conda init
echo "PS1='\w $ '" >> .bashrc
```

This will (1) initialize Conda and (2) modify your shell settings to a cleaner prompt.

Now close & reopen your terminal or run `source ~/.bashrc` (or whatever configuration file you have, such as `.profile`).

If this gives you an error, do NOT proceed. Ask the cluster overseer for help.

## Set up your channels

To make sure all our software installs correctly, let's start by configuring software sources:

```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
```

## Mamba

The default package resolver has been known to have some issues. As such, whenever you do a Conda install, you should instead use Mamba. You can install Mamba with the following command:

```
conda install mamba -n base -c conda-forge
```

You are now ready to start creating environments. From this point forward, I recommend looking at the [Conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for how to create environments, activate them, deactivate them, and more.