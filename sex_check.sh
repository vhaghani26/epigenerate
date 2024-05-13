#!/bin/bash

# Function to determine the chromosome notation used in the BAM file
detect_chromosome_notation() {
    # Run idxstats on the BAM file and check if any chromosome starts with "chr"
    if samtools idxstats "$1" 2>/dev/null | awk '$1 ~ /^chr/{exit 0} END{exit 1}'; then
        echo "chrX"
    elif samtools idxstats "$1" 2>/dev/null | awk '$1 == "chrY"{exit 0} END{exit 1}'; then
        echo "chrY"
    else
        echo "X"
    fi
}

# Function to calculate coverage statistics
coveragestats() {
    samtools idxstats "$1" 2>/dev/null | awk -v chr_notation="$2" '$1==chr_notation{print $3}'
}

# Set the directory containing BAM files
bam_dir="."

# Iterate over all BAM files in the directory
for bam_file in "$bam_dir"/*.bam; do
    # Extract sample name from the BAM file name
    sample=$(basename "$bam_file" .bam)

    # Check if the BAM file exists
    if [ -f "$bam_file" ]; then
        # Determine chromosome notation used in the BAM file
        chromosome_notation=$(detect_chromosome_notation "$bam_file")

        # Calculate coverage statistics
        xcov=$(coveragestats "$bam_file" "$chromosome_notation")
        ycov=$(coveragestats "$bam_file" "Y")
        total_xy_reads=$(echo "$xcov + $ycov" | bc)
        
        # Check if X and Y coverage information is available
        if [ -n "$xcov" ] && [ -n "$ycov" ]; then
            # Calculate ratios
            x_to_y_ratio=$(echo "scale=2; $xcov / $ycov" | bc)
            y_to_x_ratio=$(echo "scale=2; $ycov / $xcov" | bc)
            
            # Calculate proportion of reads from X and Y chromosomes
            proportion_x=$(echo "scale=5; ($xcov / $total_xy_reads) * 100" | bc)
            proportion_y=$(echo "scale=5; ($ycov / $total_xy_reads) * 100" | bc)

            # Determine suspected sex
            suspected_sex=""
            if (( $(echo "$proportion_y >= 1" | bc -l) )); then
                suspected_sex="Male"
            else
                suspected_sex="Female"
            fi

            # Output result
            echo "$sample:"
            echo "     X: $xcov"
            echo "     Y: $ycov"
            echo "     Proportion of Reads from X: $proportion_x%"
            echo "     Proportion of Reads from Y: $proportion_y%"
            echo "     X/Y Ratio: $x_to_y_ratio"
            echo "     Y/X Ratio: $y_to_x_ratio"
            echo "     Suspected Sex: $suspected_sex"
        else
            echo "Coverage statistics for $sample are missing. Cannot determine sex."
        fi
    else
        echo "BAM file $bam_file does not exist."
    fi
done
