# Using R on Epigenerate

## Setting up Libraries

By now, you should know that your actual home directory on epigenerate is not where you should be working. You should be working in `/share/lasallelab/{your_directory}`. The problem with this is that R does not know that, so you have to tell it you're working here.

First, you need to create a folder under your personal directory called `rlibs/`.

```
mkdir /share/lasallelab/{your_directory}/rlibs
```

I don't know if it's strictly necessary to enter the directory, but I recommend entering it and running the following:

```
export R_LIBS_USER="/share/lasallelab/{your_directory}/rlibs"
```

Now restart your terminal.


## Running R

Enter your LaSalle lab directory and run `module load R` to activate R and run it interactively. You can also run entire scripts using:

```
Rscript example.R
```
