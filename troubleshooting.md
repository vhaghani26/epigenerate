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

Fix: ???

## Comethyl