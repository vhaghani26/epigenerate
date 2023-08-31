# Using R on Epigenerate

## Setting up Libraries

By now, you should know that your actual home directory on epigenerate is not where you should be working. You should be working in `/share/lasallelab/{your_directory}`. The problem with this is that R does not know that, so you have to tell it you're working here.

First, you need to create a folder under your personal directory called `rlibs/`.

```
mkdir /share/lasallelab/{your_directory}/rlibs
```

Then add the following to your `.profile`, `.bashrc`, or whatever file you use.

```
export R_LIBS_USER="/share/lasallelab/{your_directory}/rlibs"
```

Now restart your terminal or source the file you added the path to.


## Running R Interactively

Enter your LaSalle lab directory and run `module load R` to activate R and run it interactively. 

## Running R via the Command Line

You can run entire scripts using:

```
Rscript example.R
```

## Conda for R

Make sure that you already have Conda set up for Epigenerate using [these instructions](https://github.com/vhaghani26/epigenerate/blob/main/conda.md). Once you have conda set up, create an environment.

```
conda create r_example
```

Activate the environment

```
conda activate r_example
```

Now install R. You can specify the version of R if needed like so:

```
conda install r-base=4.1.2
```

Or just run the following to get the most recent version:

```
conda install r-base
```

In order to install R packages (i.e. those that typically use **`install.packages()`**, use the following notation:

```
conda install -c conda-forge r-{package_name}
```

The package name should be all lowercase like so:

```
conda install -c conda-forge r-tidygraph
```

Here are some other examples:

```
conda install -c conda-forge r-remotes
conda install -c conda-forge r-xml2
conda install -c conda-forge r-igraph
conda install -c conda-forge r-reticulate
conda install -c conda-forge r-v8
conda install -c conda-forge r-ggraph
conda install -c conda-forge r-umap
conda install -c conda-forge r-treemap
conda install -c conda-forge r-juicyjuice
conda install -c conda-forge r-rcpptoml
```

If you want to use a Bioconductor package, first run the following to set up Bioconductor (note that I don't know _exactly_ what this is doing, but it works when I run it and lets me use Bioconductor packages, so just run it):

```
conda install -c conda-forge r-biocmanager
conda install -c bioconda bioconductor-biocversion
conda install bioconductor-biocparallel
```

Now you can install Bioconductor packages using this notation, again with the names being all lowercase:

```
conda install -c bioconda bioconductor-{bioconductor_package}
```

Here are some examples:

```
conda install -c bioconda bioconductor-chipseeker
conda install -c bioconda bioconductor-rrvgo
conda install -c bioconda bioconductor-pcatools
conda install -c bioconda bioconductor-enrichplot
```

## Using R on Epigenerate

Interactive R sessions for visualization are often essential, justifying the existence of tools like RStudio. But imagine having a directory filled with sizable data files that need visualizing in R. Do you shuttle individual files to your local computer for analysis? And if these files are massive, what then? Alternatively, would you script and run R operations on Epigenerate, continuously transferring figures to verify accuracy? While these methods function, they're cumbersome and inefficient. A more streamlined approach involves launching an interactive R session, akin to RStudio, via the command line to remotely access those substantial files. Ordinarily, you can set up and initiate an interactive RStudio session using rstudio-server. However, due to limited permissions, this isn't always feasible. My attempt to install and launch rstudio-server resulted in a discouraging "This incident will be reported." Given the extensive data awaiting visualization, this limitation proved exceedingly frustrating. Consequently, in my usual fashion, I invested significant effort into devising a workaround that enables you to run R and observe visualizations in real-time, all while leveraging Epigenerate's data-saving and storage capabilities. Without further ado, let's dive in!

First, create a symbolic link to `/share/lasallelab/` in your home directory:

```
cd ~
ln -s /share/lasallelab/ lasallelab
```

Now create or enter a Conda environment of your choosing, you will need to install Jupyter, R, and IRkernel (which allows you to launch a Jupyter notebook and run R). To do so, run the following:

```
conda install -c anaconda jupyter
conda install r-base
conda install -c conda-forge r-irkernel
R -e "IRkernel::installspec(user = FALSE)" # I'm not sure what this does, but I ran it and things worked out in the end so I guess just trust me for now?
```

Then launch Jupyter Notebook:

```
jupyter notebook
```

A screen will open displaying a link that starts with something like `http://localhost:8888/`. Keep that aside for now. Open a new terminal and do **not** log into Epigenerate. Instead, you will tunnel into the session. Run the following:

```
ssh -L 8888:localhost:8888 {your_username}@epigenerate.genomecenter.ucdavis.edu
```

Enter your password when prompted. Now go back to the other terminal with the link and copy and paste it into your browser. It should open a Jupyter notebook. In order to access the shared space, click on the `lasallelab` symbolic link you made. It will take you to `/share/lasallelab/`. Enter the directory you want to work and save your files to. Click on "New" in the upper right-hand corner and click "R" for an R notebook. Name your notebook and save it, then you're good to go!

There are actually other things this may be useful for as well, such as navigating your files easily, uploading files, downloading files, opening HTML files, looking at saved figures, etc. The world is your oyster. 