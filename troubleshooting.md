# Troubleshooting

## General Troubleshooting Tips

### Conda Load In

Input:

```
module load conda

# Your script
```

Error:

```
CondaError: Run 'conda init' before 'conda activate'
```

Fix: You need to read source the conda shell function loader

```
# Load conda
module load conda

#  Source the Conda shell function loader
source /cvmfs/hpc.ucdavis.edu/sw/conda/root/etc/profile.d/conda.sh

# Activate the conda environment
conda activate your_environment
```

## DMRichR

### MatrixGenerics

Error:
```
Error in MatrixGenerics:::.load_next_suggested_package_to_search(x) :
  Failed to find a rowSums2() method for list objects.
Calls: <Anonymous> ... <Anonymous> -> <Anonymous> -> <Anonymous> -> <Anonymous>
Execution halted
```

Fix: ??? \
I encountered MatrixGenerics error  due to inconsistent seqname style. When working with the "rheMac10" genome, CpG reports from Bismark have "NC_" style chromosome names (e.g., NC_041754.1), but DMRichR expects chr style names (e.g., chr1, chr2).

You can fix this by remapping the chromosome names using the UCSC–RefSeq conversion file (ucsdtorefseq_rheMac10.txt), which looks like:

chr1    0   223616942   NC_041754.1 \
chr2    0   196197964   NC_041755.1 \
...

Fix All CpG Reports in a Directory:

```
for f in *_CpG_report.txt.gz
do
    out=${f%_CpG_report.txt.gz}.chr.CpG_report.txt.gz
    echo "Converting $f → $out"
    zcat "$f" | \
    awk 'NR==FNR {map[$4]=$1; next} {if($1 in map) $1=map[$1]; print}' \
        ucsdtorefseq_rheMac10.txt - | \
    gzip > "$out"
done
```
This will produce new files named like {sample}.chr.CpG_report.txt.gz with the correct chr style names that DMRichR recognizes.

## Comethyl
