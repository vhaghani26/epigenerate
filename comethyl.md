# Using Comethyl on Epigenerate

Once you have generated your Cytosine Reports, you may run [Comethyl](https://github.com/cemordaunt/comethyl)! Note that it may be easier to run this in a screen.

1. Navigate to your project directory and create a new directory where we will put the Comethyl outputs

```
cd /share/lasallelab/{your_name}/{your_project}/
mkdir Comethyl_Results
```

2. Enter the new directory. We are going to create a cache directory and grant it full permissions for Comethyl to cache things to

```
cd Comethyl_Results
mkdir .cache
chmod 777 -R .cache/
```

3. Create your Sample Trait Table (`sample_info.xlsx` file) and put it in `Comethyl_Results/`. Please refer to the Comethyl documentation on [creating your Sample Trait Table](https://cemordaunt.github.io/comethyl/articles/comethyl.html). Note that because it's in `xlsx` format, it may be easier to create it on your local machine and `scp` or `rsync` it into the directory on Epigenerate.

4. Initiate an `srun` session:

```
srun --mem=50G --time=5:00:00 --pty /bin/bash
```

5. Activate the Comethyl conda environment 

```
conda activate /share/lasallelab/programs/.conda/Comethyl_v1.3.0
```

6. Activate R

```
R
```

7. Set your library path

```
.libPaths("/share/lasallelab/programs/.conda/Comethyl_v1.3.0/lib/R/library")
```

8. Set the cache directory to the one we made

```
AnnotationHub::setAnnotationHubOption("CACHE", value = "/share/lasallelab/{your_name}/{your_project}/Comethyl_Results/.cache")
```

9. Load the necessary libraries

```
library(tidyverse)
library(comethyl)
```

10. Set your global options

```
options(stringsAsFactors = FALSE)
Sys.setenv(R_THREADS = 1)
WGCNA::disableWGCNAthreads()
```

11. Read the Bismark CpG reports. For the first command, it runs assuming the cytosine reports are in your current working directory. To mimic this, we will briefly change our working directory, then change back after we read in what we need.

```
colData <- openxlsx::read.xlsx("sample_info.xlsx", rowNames = TRUE)
setwd("/share/lasallelab/{your_name}/{your_project}/08_cytosine_reports/")
bs <- getCpGs(colData, file = "Unfiltered_BSseq.rds")
setwd("/share/lasallelab/{your_name}/{your_project}/Comethyl_Results/")
```

12. Examine CpG Totals at Different Cutoffs

```
CpGtotals <- getCpGtotals(bs, file = "CpG_Totals.txt")
plotCpGtotals(CpGtotals, file = "CpG_Totals.pdf")
```

13. Filter the BS object. This is the first point you will have the opportunity to make decisions about the parameters. Please reference the original documentation for [Comethyl](https://github.com/cemordaunt/comethyl) to adjust parameters as needed. 

```
bs <- filterCpGs(bs, cov = 2, perSample = 0.75, file = "Filtered_BSseq.rds")
```

14. Call regions

```
regions <- getRegions(bs, file = "Unfiltered_Regions.txt")
plotRegionStats(regions, maxQuantile = 0.99, file = "Unfiltered_Region_Plots.pdf")
plotSDstats(regions, maxQuantile = 0.99, file = "Unfiltered_SD_Plots.pdf")
```

15. Examine Region Totals at Different Cutoffs

```
regionTotals <- getRegionTotals(regions, file = "Region_Totals.txt")
plotRegionTotals(regionTotals, file = "Region_Totals.pdf")
```

16. Filter regions. At this step, you have another opportunity to change parameters to better fit your needs. Typically, we do 500000 regions. However, this was with the constraints of the old epigenerate's computational power. As such, you have some room for exploration here.

```
regions <- filterRegions(regions, covMin = 10, methSD = 0.05,
                         file = "Filtered_Regions.txt")
plotRegionStats(regions, maxQuantile = 0.99, file = "Filtered_Region_Plots.pdf")
plotSDstats(regions, maxQuantile = 0.99, file = "Filtered_SD_Plots.pdf")
```

17. Adjust methylation data for PCs. This is the last step we will run with `srun` before switching to an `sbatch` submission. 

```
meth <- getRegionMeth(regions, bs = bs, file = "Region_Methylation.rds")
mod <- model.matrix(~1, data = pData(bs))

PCs <- getPCs(meth, mod = mod, file = "Top_Principal_Components.rds")
PCtraitCor <- getMEtraitCor(PCs, colData = colData, corType = "bicor",
                            file = "PC_Trait_Correlation_Stats.txt")
PCdendro <- getDendro(PCs, distance = "bicor")
PCtraitDendro <- getCor(PCs, y = colData, corType = "bicor", robustY = FALSE) %>%
        getDendro(transpose = TRUE)
plotMEtraitCor(PCtraitCor, moduleOrder = PCdendro$order,
               traitOrder = PCtraitDendro$order,
               file = "PC_Trait_Correlation_Heatmap.pdf")

methAdj <- adjustRegionMeth(meth, PCs = PCs,
                            file = "Adjusted_Region_Methylation.rds")
getDendro(methAdj, distance = "euclidean") %>%
        plotDendro(file = "Sample_Dendrogram.pdf", expandY = c(0.25, 0.08))
```

18. Once you are done, fully exit. Quit R using `q()`, then end your `srun` session using `exit`.

19. Create a new file called `softpower_modules.R` and put the following in it. Make sure to edit the cache path on the third line.

```
# Set library path
.libPaths("/share/lasallelab/programs/.conda/Comethyl_v1.3.0/lib/R/library")
AnnotationHub::setAnnotationHubOption("CACHE", value = "/share/lasallelab/{your_name}/{your_project}/Comethyl_Results/.cache")

# Load libraries
library(tidyverse)
library(comethyl)

# Set global options
options(stringsAsFactors = FALSE)
Sys.setenv(R_THREADS = 1)
WGCNA::disableWGCNAthreads()

# Load objects
methAdj <- readRDS("Adjusted_Region_Methylation.rds")
regions <- read.delim("Filtered_Regions.txt")

# Select Soft Power Threshold ####
sft <- getSoftPower(methAdj, corType = "pearson", file = "Soft_Power.rds")
plotSoftPower(sft, file = "Soft_Power_Plots.pdf")

# Get Comethylation Modules ####
modules <- getModules(methAdj, power = sft$powerEstimate, regions = regions,
                      corType = "pearson", file = "Modules.rds")
plotRegionDendro(modules, file = "Region_Dendrograms.pdf")
BED <- getModuleBED(modules$regions, file = "Modules.bed")
```

20. Create a slurm file

```
nano {project_name}_comethyl.slurm
```

21. Add the job details to your slurm file and save the file. Here is a SLURM script template for you to use that allows for the usage of the Comethyl environment. Make sure to make the following changes:

* Change `{your_email}` to your email
* Fix the path listed under `--chdir` to update the working directory
* Change `source ~/.profile` if you use a different configuration file (if you set up Conda with Viki, you use .profile)

```
#!/bin/bash
#
#SBATCH --job-name=comethyl            											# Job name
#SBATCH --mail-user={your_email}       											# Your email
#SBATCH --ntasks=70                    											# Number of cores/threads
#SBATCH --mem=800000                   											# Ram in Mb
#SBATCH --partition=production         											# Partition, or queue, to assign to
#SBATCH --time=3-00:00:00              											# Time requested for job
#SBATCH --mail-type=ALL                											# Get an email when the job begins, ends, or fails
#SBATCH --chdir=/share/lasallelab/{your_name}/{your_project}/Comethyl_Results/	# Your working directory

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

# Run aklog to deal with SLURM bug
aklog

# Source your config file so conda can be used (likely .profile, could be .bashrc)
source ~/.profile

# Activate the conda environment
conda activate /share/lasallelab/programs/.conda/Comethyl_v1.3.0

##############
## Comethyl ##
##############

Rscript softpower_modules.R

###################
# Run Information #
###################

end=`date +%s`
runtime=$((end-start))
echo $runtime
```

22. Submit the job

```
sbatch {project_name}_comethyl.slurm
```

23.. Depending on how the SLURM script was edited, there may be an error that says something about "DOS line break error." If this occurs, run:

```
dos2unix {project_name}_comethyl.slurm
```

And then resubmit the script. You will receive email notifications when your job starts and ends and if it fails.
 
