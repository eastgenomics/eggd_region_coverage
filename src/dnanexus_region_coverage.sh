#!/bin/bash
set -e -x -o pipefail

# Generated by dx-app-wizard.
#
# Basic execution pattern: Your app will run on a single machine from
# beginning to end.
#
# Your job's input variables (if any) will be loaded as environment
# variables before this script runs.  Any array inputs will be loaded
# as bash arrays.
#
# Any code outside of main() (or any entry point you may add) is
# ALWAYS executed, followed by running the entry point itself.
#
# See https://documentation.dnanexus.com/developer for tutorials on how
# to modify this file.

main() {

    echo "Value of input_bam: '$input_bam'"
    echo "Value of bam_index: '$bam_index'"
    echo "Value of input_bed: '$input_bed'"
    echo "Value of flank: '$flank'"
    echo "Value of F: '$F'"

    # The following line(s) use the dx command-line tool to download your file
    # inputs to the local file system using variable names for the filenames. To
    # recover the original filenames, you can use the output of "dx describe
    # "$variable" --name".

    echo "downloading input data"

    dx download "$input_bam" -o input_bam
    dx download "$bam_index" -o input_bam.bai
    dx download "$input_bed" -o input_bed

    # Fill in your application code here.
    echo "installing dependencies"

    pip install pip-20.3.3.tar.gz
    pip install pysam-0.7.6.tar.gz

    echo "running coverage calculations"

    sample_output=${input_bam_prefix}.nirvana_2010_5bp
    ./region_coverage.py -F -f $flank -b input_bam -B input_bed -o $sample_output

    echo "uploading results"

    coverage_output=$(dx upload ${sample_output}.gz --brief)
    coverage_index=$(dx upload ${sample_output}.gz.tbi --brief)

    # The following line(s) use the utility dx-jobutil-add-output to format and
    # add output variables to your job's output as appropriate for the output
    # class.  Run "dx-jobutil-add-output -h" for more information on what it
    # does.

    dx-jobutil-add-output coverage_output "$coverage_output" --class=file
    dx-jobutil-add-output coverage_index "$coverage_index" --class=file

    echo "done"
}
