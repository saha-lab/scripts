#!/usr/bin/env python

"""
This assumes that picard tools is installed and are in the PATH environment 
(can be run using 'picard' from the terminal).

This script recursively gets all of the bam files from the current directory and 
any subdirectories and then runs the picard tools CleanSam script in order to 
soft-clipping beyond-end-of-reference alignments and setting MAPQ to 0 for unmapped reads.
This needs to be done before running BAMQC on a bam file.

USAGE: iterate_cleanbam.py <input_dir>
Output: cleaned bam files in origin directory

Updated 180311 by Ronald Cutler

TODO: Parallelize this process to run multiple instances of picard CleanSam
"""

import os, sys
from glob import glob


def main(inDir):
	matches = [y for x in os.walk(inDir) for y in glob(os.path.join(x[0], '*coord_sort.bam'))]
 
	print ("\nFiles to be cleaned...")
	for file in matches:
		print (file)

	for file in matches:
		outfile = file + "_cleaned.bam"
		os.system('picard CleanSam I={0} O={1}'.format(file, outfile))
		print ("Done cleaning", file)

if __name__ == "__main__":
	main(sys.argv[1])