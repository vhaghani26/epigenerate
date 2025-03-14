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

As mentioned in the epigenerate documentation, you should be using conda. First, go to the [Anaconda website](https://www.anaconda.com/download#downloads). Right-click or control-click on Windows or MacOS, respectively, on the latest Anaconda installer listing under the "Linux" section. Click "copy link" and run the following, making sure to modify the path and enter the link:

```
# Navigate to  your home directory
cd ~
# Download Anaconda
wget {copied_link}
```

This will download a file that look something like `Anaconda3{somestuff}.sh`. Run the script:

```
bash Anaconda3{somestuff}.sh
```

Read the license agreement and answer "yes" (without quotes) to accept the terms. Accept all defaults. It will take a little time to install. When the installer asks if you want to initialize Anaconda3 by running conda init, answer "yes."

Now you have Conda installed! Add the following to your `.bashrc` or `.profile` or whatever you're using. Make sure to replace all variables within the curly brackets `{}` appropiately. Your Conda prefix is `home/{your_username}/anaconda3`.

```
# Paths for conda and software configuration
export LASALLEHOME=/quobyte/lasallegrp/{your_folder}

# Aliases to improve CLI usage experience
alias ls="ls -F"
alias rm="rm -i"
alias cp="cp -i"
alias mv="mv -i"

# Reconfigure command line display
PS1='\u@\h: \W:\$ '

# Execute conda setup 
__conda_setup="$('{conda_prefix}/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
        eval "$__conda_setup"
else
        if [ -f "{conda_prefix}/etc/profile.d/conda.sh" ]; then
                . "{conda_prefix}/etc/profile.d/conda.sh"
        else
                export PATH="{conda_prefix}/bin:$PATH"
        fi
fi
unset __conda_setup
```

Once done, copy the above code into your `.bashrc` or `.profile` (or whatever other configuration file you use on epigenerate). This file will be found in your home directory. 

## Initialize Conda

If you did not initialize Conda when you installed it, run the following:

```
conda init
```

This will initialize Conda. Now close & reopen your terminal or run `source ~/.bashrc` (or whatever configuration file you have, such as `.profile`).

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

From this point forward, just use `mamba` instead of `conda` with your install commands. You are now ready to start creating environments. 

## Using Conda

From this point forward, I recommend looking at the [Conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for how to create environments, activate them, deactivate them, and more.

Given that we all used shared software, there are environments you are able to activate and use in `/share/lasallelab/programs/.conda/`, namely `epigenerator`. If you want to activate these environments, you will need to use the full file path:

```
conda activate /share/lasallelab/programs/.conda/epigenerator
```

Otherwise, it will activate the Conda using your Conda prefix.