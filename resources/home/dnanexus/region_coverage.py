#!/usr/bin/python2

import pprint
import os
import argparse
pp = pprint.PrettyPrinter(indent=4)

import pysam

BIN_0_MIN  = -10
BIN_0_MAX  = 0

BIN_1_MIN  = 1
BIN_1_MAX  = 5

BIN_2_MIN  = 6
BIN_2_MAX  = 9

BIN_3_MIN  = 10
BIN_3_MAX  = 19

FLANK      = 0



# 
# 
# 
# Kim Brugger (29 May 2012)
def numbers2ranges(chrom, depths):

  bin0 = []
  bin1 = []
  bin2 = []
  bin3 = []
  bin4 = []
  for offset in range(0, len(depths)):

    depth = depths[offset]

    if ( depth >= BIN_0_MIN and depth <= BIN_0_MAX):
      bin0.append( offset + flank_region_start + 1)

    elif ( depth >= BIN_1_MIN and depth <= BIN_1_MAX):
      bin1.append( offset + flank_region_start + 1)

    elif ( depth >= BIN_2_MIN and depth <= BIN_2_MAX):
      bin2.append( offset + flank_region_start + 1)

    elif ( depth >= BIN_3_MIN and depth <= BIN_3_MAX):
      bin3.append( offset + flank_region_start + 1)
    else:
      bin4.append( offset + flank_region_start + 1)


  return "\t".join([_numbers2ranges(chrom, bin0), _numbers2ranges(chrom, bin1), _numbers2ranges(chrom, bin2), _numbers2ranges(chrom, bin3)])


def _numbers2ranges(chrom, positions):

  res = []
  (start, end) = (-1,-1)

  for pos in positions:
    if ( start == -1):
      start = pos
      end = pos

    if (pos > end + 1):
      res.append("%s:%d-%d" % (chrom, start, end))
      start = pos

    end = pos

  if ( end != -1 ):
    res.append("%s:%d-%d" % (chrom, start, end))

  return ",".join( res )



if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Calculates the coverage for regions. Not the input is 0 based and the end is  non-inclusive and the output is 1 based with both ends included in the region specification.')
        
    parser.add_argument('-b','--bam', help='Bam file to calculate from')
    parser.add_argument('-B','--bed', help='Bed containing regions to look at')
    parser.add_argument('-o','--outfile', help='File to write to, if done it will be compressed and indexed as well')
    parser.add_argument('-f', '--flank', type=int, default=5,  help="flanks added to regions, default 5bp")
    parser.add_argument('-F', '--force-overwrite', action="store_true", default=False,  help="overwrite old file if present")
    
    args = parser.parse_args()

    if ( args.bam is None or args.bed is None):
        parser.parse_args(['-h'])
        exit()

    samfile = pysam.Samfile( args.bam, "rb" )
    bedfile_fh = open(args.bed, "r")

    fh = None
    if args.outfile is not None:
      if os.path.isfile( "{}.gz".format( args.outfile )) and not args.force_overwrite:
        print("Error, out file {} already exists, to overwrite use the -F flag".format( args.outfile))
        exit(-10)
      fh = open( args.outfile, 'w')
      

    if ( fh is not None):
      fh.write("# File generated by region_coverage.py\n")
      fh.write("# Args: -b {} -B {} -f {}\n".format(args.bam, args.bed, args.flank))
    else:
      print("# File generated by target_depths")
      print("# Args: -b {} -B {} -f {}".format(args.bam, args.bed, args.flank))

    # This should really be read in in bulk and sorted by the program.
    for entry in bedfile_fh.readlines():
      entry = entry.rstrip()
      (region_chrom, region_start, region_end, region_region_id) = entry.split("\t")[0:4]
      # This is now expecting a real bedfile BED. so add one to
      # the start as it is 0 based, and the end is non-inclusive in
      # the specification.
      region_start = int(region_start) + 1
      region_end   = int(region_end) 
      flank_region_start = region_start  - args.flank - 1
      flank_region_end   = region_end    + args.flank - 1
      
      depths = [ 0 ] * (flank_region_end - flank_region_start + 1 )
      for x in samfile.pileup(region_chrom, flank_region_start, flank_region_end ):

        pileup_pos   = int(x.pos)
        
        if ( pileup_pos < flank_region_start or pileup_pos > flank_region_end):
          continue

        depths[ pileup_pos - flank_region_start ] = x.n

      min_depth  = min(depths)
      mean_depth = "{:.2f}".format(sum(depths)*1.0/(flank_region_end - flank_region_start + 1 ))
      max_depth  = max(depths)


      if ( fh is not None ):
        fh.write("\t".join([ region_chrom, str( region_start), str(region_end), str(min_depth), mean_depth, str(max_depth), numbers2ranges(region_chrom, depths)]) +"\n")
      else:
        print "\t".join([ region_chrom, str( region_start), str(region_end),  str(min_depth), mean_depth, str(max_depth), numbers2ranges(region_chrom, depths)])

    if ( fh is not None):
      fh.close()
      pysam.tabix_index(args.outfile, seq_col=0, start_col=1, end_col=2, force=args.force_overwrite)






