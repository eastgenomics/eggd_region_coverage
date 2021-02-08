<!-- dx-header -->
# Single-sample region coverage (DNAnexus Platform App)

<!-- Insert a description of your app here -->

This is the source code for an app that runs on the DNAnexus Platform.
For more information about how to run or modify it, see
https://documentation.dnanexus.com/.

## What does this app do?
Calculates the coverage of specified regions in a sample.

## What are the typical use cases for this app?
To visualise QC reports, this app should be run at the end of an NGS pipeline, when all QC software outputs are available.

## What data are required for this app to run?
* sample bam and index files (.bam and .bai)
* bed file with regions of interest (0-based bed, no headers, chromosome column only contains chrom number)

Optional inputs:
* flank (int) number of bases to be looked at adjacent to the 5', 3' ends
* F (true/FALSE) whether to force overwrite output files of the same name

## What does this app output?
* A compressed and indexed coverage file
* A coverage index file (tabix)

## How does this app work?
The python script goes through the regions in the bed file and calculates min, mean, max coverage of the sample at the region from the bam and bai files.

### This app was made by East GLH
