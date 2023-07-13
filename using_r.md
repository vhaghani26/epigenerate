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
