# Using Comethyl on Epigenerate

## Prerequisites

In order to run [Comethyl](https://github.com/cemordaunt/comethyl), you should have run [epigenerator](https://github.com/vhaghani26/epigenerator) and genereated your cytosine reports. 

## Viki, do we _really_ have to do it like this now??

I'm sorry, but yes. Due to the Genome Center HPC's switch to `sbatch` and `srun` instead of running things on the head node (i.e. `epigenerate`), this introduces some complications to the workflow, as Comethyl was written to suit the architecture of the old `epigenerate` head node. One of the biggest complications is that Comethyl requires many more steps than DMRichR, many of which require optimization based on your data, suggesting that there should be an interactive approach while going through these steps. We have addressed this by encouraging the use of `srun` so you can change parameters as needed. 

However, one of the other complications is that there are a few steps that are extremely resource intensive (and used to be responsible for crashing our head node). Because you can only launch an interactive session (i.e. `srun`) in a more immediate manner, requesting a large amount of resources with `srun` may mean you will wait an irritating amount of time before you are allocated the resources you need. Additionally, there is less control over when the session will begin. Hello midnight coding session! (FYI - this chips into your requested time). As such, we have taken that specific portion of the pipeline and adapted it to run on SLURM. I understand the back and forth between submitting a SLURM script vs. using `srun` may be irritating, but given the new architecture of the HPC, I believe this is the most efficient and appropriate means of running Comethyl.

## Overview

In its essence, Comethyl will get run in 3 parts:

* An `srun` session
* A SLURM script submission
* A final `srun` session (optionally local)

You will already be familiar with the code if you have run it before. The biggest difference now is that you will change how/where you run the code.

## Running Comethyl

### Set-Up

1. Navigate to your project directory and create a new directory where we will put the Comethyl outputs

```
cd /share/lasallelab/{your_name}/{your_project}/
mkdir Comethyl_Results
```

2. Enter the new directory. We are going to create a cache directory and grant it full permissions for Comethyl to cache things to. This needs to be done because the native cache directory in your true home directory leads to permission issues that will cause Comethyl to fail. By telling it explicitly to cache somewhere else, we will not run into that issue

```
cd Comethyl_Results
mkdir .cache
chmod 777 -R .cache/
```

3. Create your Sample Trait Table (`sample_info.xlsx` file) and put it in `Comethyl_Results/`. Please refer to the Comethyl documentation on [creating your Sample Trait Table](https://cemordaunt.github.io/comethyl/articles/comethyl.html). Note that because it's in `xlsx` format, it may be easier to create it on your local machine and `scp` or `rsync` it into the directory on Epigenerate.

### First `srun` Session

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
WGCNA::disableWGCNAThreads()
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

### SLURM Submission

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

23. Depending on how the SLURM script was edited, there may be an error that says something about "DOS line break error." If this occurs, run:

```
dos2unix {project_name}_comethyl.slurm
```

And then resubmit the script. You will receive email notifications when your job starts and ends and if it fails.

### Second `srun` Session

Although the instructions allow for you to run Comethyl using `srun`, you may be able to run this on your local computer, as it is not resource intensive and the visualization aspect of Rstudio may be helpful. Down the line, the Genome Center HPC will have better options for visualization. That is currently (and unfortunately) not the case. If you choose to do it on your local computer, you will need to `scp` or `rsync` the `sample_info.xlsx` file you created as well as the `Modules.rds` file generated after you submit the SLURM script. You will also need to install the necessary packages (`tidyverse` and `comethyl`), which may be a pain depending on how up-to-date or out-of-date your R version is. Because R really likes to have dependency issues with any updates, I still advise using the Conda environment on `epigenerate` for consistency across your software versions, but you are still free to run it on your own computer if you're in a bind or having issues with `epigenerate`.

24. Once your SLURM job finishes, initiate another `srun` session, activate the environment, and restart R:

```
srun --mem=50G --time=5:00:00 --pty /bin/bash
conda activate /share/lasallelab/programs/.conda/Comethyl_v1.3.0
R
```

25. Reload the libraries and data needed and reset the global options

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

# Load data 
modules <- readRDS("Modules.rds")
```

26. Examine correlations between modules and samples

```
MEs <- modules$MEs
moduleDendro <- getDendro(MEs, distance = "bicor")
plotDendro(moduleDendro, labelSize = 4, nBreaks = 5,
           file = "Module_ME_Dendrogram.pdf")
moduleCor <- getCor(MEs, corType = "bicor")
plotHeatmap(moduleCor, rowDendro = moduleDendro, colDendro = moduleDendro,
            file = "Module_Correlation_Heatmap.pdf")
			
sampleDendro <- getDendro(MEs, transpose = TRUE, distance = "bicor")
plotDendro(sampleDendro, labelSize = 3, nBreaks = 5,
           file = "Sample_ME_Dendrogram.pdf")
sampleCor <- getCor(MEs, transpose = TRUE, corType = "bicor")
plotHeatmap(sampleCor, rowDendro = sampleDendro, colDendro = sampleDendro,
            file = "Sample_Correlation_Heatmap.pdf")

plotHeatmap(MEs, rowDendro = sampleDendro, colDendro = moduleDendro,
            legend.title = "Module\nEigennode",
            legend.position = c(0.37, 0.89), file = "Sample_ME_Heatmap.pdf")
```

27. Test correlations between module eigennodes and sample traits

```
MEtraitCor <- getMEtraitCor(MEs, colData = colData, corType = "bicor",
                            file = "ME_Trait_Correlation_Stats.txt")
traitDendro <- getCor(MEs, y = colData, corType = "bicor", robustY = FALSE) %>%
        getDendro(transpose = TRUE)
plotDendro(traitDendro, labelSize = 3.5, expandY = c(0.65, 0.08),
           file = "Trait_Dendrogram.pdf")
plotMEtraitCor(MEtraitCor, moduleOrder = moduleDendro$order,
               traitOrder = traitDendro$order,
               file = "ME_Trait_Correlation_Heatmap.pdf")
plotMEtraitCor(MEtraitCor, moduleOrder = moduleDendro$order,
               traitOrder = traitDendro$order, topOnly = TRUE, label.type = "p",
               label.size = 4, label.nudge_y = 0, legend.position = c(1.11, 0.795),
               colColorMargins = c(-1, 4.75, 0.5, 10.1),
               file = "Top_ME_Trait_Correlation_Heatmap.pdf", width = 8.5,
               height = 4.25)
```


28. Now we will explore significant ME-trait correlations. First, we will plot the module eigennodes vs. traits. **From this point forward**, the code serves as more of a template. You will need to adjust the modules to be your modules of interest and change the color coding to match the traits you have in your Sample Trait Table. 

```
plotMEtraitDot(MEs$bisque4, trait = colData$Diagnosis_ASD,
               traitCode = c("TD" = 0, "ASD" = 1),
               colors = c("TD" = "#3366CC", "ASD" = "#FF3366"), ylim = c(-0.2, 0.2),
               xlab = "Diagnosis", ylab = "Bisque 4 Module Eigennode",
               file = "bisque4_ME_Diagnosis_Dotplot.pdf")
plotMEtraitScatter(MEs$paleturquoise, trait = colData$Gran, ylim = c(-0.15, 0.15),
                   xlab = "Granulocytes", ylab = "Pale Turquoise Module Eigennode",
                   file = "paleturquoise_ME_Granulocytes_Scatterplot.pdf")
plotMEtraitScatter(MEs$paleturquoise, trait = colData$Bcell, ylim = c(-0.15, 0.15),
                   xlab = "B-cells", ylab = "Pale Turquoise Module Eigennode",
                   file = "paleturquoise_ME_Bcells_Scatterplot.pdf")
```

29. Plot region methylation vs. traits

```
regions <- modules$regions
plotMethTrait("bisque4", regions = regions, meth = meth,
              trait = colData$Diagnosis_ASD, traitCode = c("TD" = 0, "ASD" = 1),
              traitColors = c("TD" = "#3366CC", "ASD" = "#FF3366"),
              trait.legend.title = "Diagnosis",
              file = "bisque4_Module_Methylation_Diagnosis_Heatmap.pdf")
plotMethTrait("paleturquoise", regions = regions, meth = meth,
              trait = colData$Gran, expandY = 0.04, trait.legend.title = "Granulocytes",
              trait.legend.position = c(1.034, 3.35),
              file = "paleturquoise_Module_Methylation_Granulocytes_Heatmap.pdf")
plotMethTrait("paleturquoise", regions = regions, meth = meth,
              trait = colData$Bcell, expandY = 0.04,
              trait.legend.title = "B-cells", trait.legend.position = c(1.004, 3.35),
              file = "paleturquoise_Module_Methylation_Bcells_Heatmap.pdf")
```

30. Annotate modules

```
regionsAnno <- annotateModule(regions, module = c("bisque4", "paleturquoise"),
                              genome = "hg38",
                              file = "Annotated_bisque4_paleturquoise_Module_Regions.txt")
geneList_bisque4 <- getGeneList(regionsAnno, module = "bisque4")
geneList_paleturquoise <- getGeneList(regionsAnno, module = "paleturquoise")
```

31. Analyze functional enrichment

```
ontologies <- listOntologies("hg38", version = "4.0.4")
enrich_bisque4 <- enrichModule(regions, module = "bisque4", genome = "hg38",
                               file = "bisque4_Module_Enrichment.txt")
plotEnrichment(enrich_bisque4, file = "bisque4_Module_Enrichment_Plot.pdf")
enrich_paleturquoise <- enrichModule(regions, module = "paleturquoise",
                                     genome = "hg38",
                                     file = "paleturquoise_Module_Enrichment.txt")
plotEnrichment(enrich_paleturquoise, axis.text.y.size = 14, width = 10,
               file = "paleturquoise_Module_Enrichment_Plot.pdf")
```
