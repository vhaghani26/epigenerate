# Set library path
.libPaths("/share/lasallelab/programs/.conda/Comethyl_v1.3.0/lib/R/library")

# Set cache directory
AnnotationHub::setAnnotationHubOption("CACHE", value = "/share/lasallelab/Viki/Mouse_FAE_RNAseq_WGBS/wgbs/Comethyl_Results/.cache")

# Load libraries
library(tidyverse)
library(comethyl)
library(Biobase)

# Set global options
options(stringsAsFactors = FALSE)
Sys.setenv(R_THREADS = 1)
WGCNA::disableWGCNAThreads()

#############
### Part 1 ##
#############

# Read Bismark CpG reports
colData <- openxlsx::read.xlsx("sample_info.xlsx", rowNames = TRUE)
setwd("/share/lasallelab/Viki/Mouse_FAE_RNAseq_WGBS/wgbs/08_cytosine_reports/")
bs <- getCpGs(colData, file = "Unfiltered_BSseq.rds")
setwd("/share/lasallelab/Viki/Mouse_FAE_RNAseq_WGBS/wgbs/Comethyl_Results")

# Examine CpG totals at different cutoffs
CpGtotals <- getCpGtotals(bs, file = "CpG_Totals.txt")
plotCpGtotals(CpGtotals, file = "CpG_Totals.pdf")

# Filter BS object
bs <- filterCpGs(bs, cov = 2, perSample = 0.70, file = "Filtered_BSseq.rds")
bs <- readRDS("Filtered_BSseq.rds")

# Call regions
regions <- getRegions(bs, file = "Unfiltered_Regions.txt")
plotRegionStats(regions, maxQuantile = 0.99, file = "Unfiltered_Region_Plots.pdf")
plotSDstats(regions, maxQuantile = 0.99, file = "Unfiltered_SD_Plots.pdf")

# Examine region totals at different cutoffs
regionTotals <- getRegionTotals(regions, file = "Region_Totals.txt")
plotRegionTotals(regionTotals, file = "Region_Totals.pdf")

# Filter regions
regions <- filterRegions(regions, covMin = 8, file = "Filtered_Regions.txt")
regions <- read.delim("Filtered_Regions.txt")
plotRegionStats(regions, maxQuantile = 0.99, file = "Filtered_Region_Plots.pdf")
plotSDstats(regions, maxQuantile = 0.99, file = "Filtered_SD_Plots.pdf")

# Adjust methylation data for PCs 
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

############
## Part 2 ##
############

# Load objects
colData <- openxlsx::read.xlsx("sample_info.xlsx", rowNames = TRUE)
regions <- read.delim("Filtered_Regions.txt")
bs <- readRDS("Filtered_BSseq.rds")
methAdj <- readRDS("Adjusted_Region_Methylation.rds")

# Select Soft Power Threshold 
sft <- getSoftPower(methAdj, corType = "pearson", file = "Soft_Power.rds", blockSize = 10000)
plotSoftPower(sft, file = "Soft_Power_Plots.pdf")

# Get Comethylation Modules 
modules <- getModules(methAdj, power = sft$powerEstimate, regions = regions,
                      corType = "pearson", file = "Modules.rds", maxBlockSize = 10000, mergeCutHeight = 0.4, minModuleSize = 60)
plotRegionDendro(modules, file = "Region_Dendrograms.pdf")
BED <- getModuleBED(modules$regions, file = "Modules.bed")

############
## Part 3 ##
############

# Load objects
modules <- readRDS("Modules.rds")
colData <- openxlsx::read.xlsx("sample_info.xlsx", rowNames = TRUE)

# Examine correlations between modules and samples
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
			
# Test correlations between module eigennodes and sample traits
MEtraitCor <- getMEtraitCor(MEs, colData = colData, corType = "bicor",
                            file = "ME_Trait_Correlation_Stats.txt")
traitDendro <- getCor(MEs, y = colData, corType = "bicor", robustY = FALSE) %>%
        getDendro(transpose = TRUE)
plotDendro(traitDendro, labelSize = 3.5, expandY = c(0.65, 0.08),
           file = "Trait_Dendrogram.pdf")
		   
# Sort Variables
sorted_trait_order <- traitDendro$order[order(traitDendro$order)]
# Get the corresponding module labels based on the order
module_order <- moduleDendro$order
ordered_module_labels <- moduleDendro$labels[module_order]
# Save ordered_module_labels to a text file
write.table(ordered_module_labels, 
            file = "ME_Trait_Correlation_Heatmap_Module_Order.txt", 
            row.names = FALSE, 
            col.names = FALSE, 
            quote = FALSE)
plotMEtraitCor(MEtraitCor, moduleOrder = moduleDendro$order,
               traitOrder = sorted_trait_order,
               colColorMargins = c(-2.5, 3.85, 2.7, 3.75),
               file = "ME_Trait_Correlation_Heatmap.pdf")
			   
plotMEtraitCor(MEtraitCor, moduleOrder = moduleDendro$order,
               traitOrder = traitDendro$order, topOnly = TRUE, label.type = "p",
               label.size = 4, label.nudge_y = 0, legend.position = c(1.11, 0.795),
               colColorMargins = c(-1, 4.75, 0.5, 10.1),
               file = "Top_ME_Trait_Correlation_Heatmap.pdf", width = 8.5,
               height = 4.25)
			   
# Explore significant ME-trait correlations
modules_of_interest <- list("honeydew1", "white", "brown", "brown4", "purple")

for (module in modules_of_interest) {
  plotMEtraitDot(MEs[[module]], 
                 trait = colData$FA_Excess,
                 traitCode = c("Control" = 0, "FA_Excess" = 1),
                 colors = c("Control" = "#3366CC", "FA_Excess" = "#FF3366"), 
                 ylim = c(-0.2, 0.2),
                 xlab = "Treatment", 
                 ylab = paste(module, "Module Eigennode"),
                 file = paste(module, "_ME_Dotplot.pdf", sep = ""))
}
			   
for (module in modules_of_interest) {
  plotMEtraitScatter(MEs[[module]], 
                     trait = colData$FA_Excess, 
                     ylim = c(-0.15, 0.15),
                     xlab = "FA_Excess", 
                     ylab = paste(module, "Module Eigennode"),
                     file = paste(module, "_ME_Scatterplot.pdf", sep = ""))
}

			   
# Plot region methylation vs traits
regions <- modules$regions
meth <- readRDS("Region_Methylation.rds")

for (module in modules_of_interest) {
  plotMethTrait(module, 
                regions = regions, 
                meth = meth,
                trait = colData$FA_Excess, 
                traitCode = c("Control" = 0, "FA_Excess" = 1),
                traitColors = c("Control" = "#3366CC", "FA_Excess" = "#FF3366"),
                trait.legend.title = "Treatment",
                file = paste(module, "_Module_Methylation_Treatment_Heatmap.pdf", sep = ""))
}

############
## Part 4 ##
############

# Move onto 02_Kostas_Comethyl.ipynb