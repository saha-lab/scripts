#!/usr/bin/env python

import os, sys, fnmatch


def main(inDir):
	bam = [x[0] for x in os.walk(inDir)]
	bam.pop(0)
	
	matches = []
	for root, dirnames, filenames in os.walk(inDir):
		for filename in fnmatch.filter(filenames, '*coord_sort.bam'):
			matches.append(os.path.join(root, filename))
 
	print("Files to be cleaned:")
	for file in matches:
		print(file)

	for file in matches:
		outfile = file + "_cleaned.bam"
		os.system('java -jar /Users/margaretsaha/Downloads/Software/picard.jar CleanSam I={0} O={1}'.format(file, outfile))
		print("Done cleaning", file)

if __name__ == "__main__":
	main(sys.argv[1])