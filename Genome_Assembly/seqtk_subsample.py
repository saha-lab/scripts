#!/usr/bin/env python
"""
Runs seqtk, a subsampling tool, on a folder of fastq files and outputs them in the same folde.
This is for paired-end reads as fastq files are run in pairs with the same seed to make sure
that randomly sampled reads are still paired.

Note seqtk must be installed and able to be called in the terminal.

USAGE: seqtk_subsample.py <decimal_fraction, e.g. 0.8> <inDir>

Updated 180202 by Ronald Cutler
"""
import os
import sys, random, itertools

def Subsample_fastq(fraction, inFolder):
	#makes a list for all the files within a folder, also will walk through folders within the folder 
	folders = [os.path.join(root, name)
	             for root, dirs, files in os.walk(inFolder)
	             for name in files
	             if name.endswith(".fq") or name.endswith(".fastq")] 

	#within the sample file, need to go into results folder to get the .fastq file 
	print("fastq files being ran through")
	for files in folders:
		print(files)

	seed = '10' # this is set so that the same reads are sampled from each paired-end fastq

	for v, w in zip(folders[::2], folders[1::2]):
		in1 = v 
		in2 = w

		output1 = in1 + "_sub_sample_" + str(fraction) + ".fastq"
		output2 = in2 + "_sub_sample_" + str(fraction) + ".fastq"

		print ("\nMate 1 is", v)
		print ("Mate 2 is", w)

		#get the total number of reads in both files

		total_in1 = os.system("grep -c '' {0}".format(in1))/4
		total_in2 = os.system("grep -c '' {0}".format(in2))/4

		if total_in1 != total_in1:
			print ("The total amount of reads in these paired-end files don't match!")
			sys.exit()

		print ("Total paired-end reads =", total_in2)
		
		#run seqtk
		os.system('seqtk sample -s {0} {1} {2} > {3}'.format(seed, in1, fraction, output1))
		os.system('seqtk sample -s {0} {1} {2} > {3}'.format(seed, in2, fraction, output2))

if __name__ == "__main__":
	fraction = sys.argv[1]
	inFolder = sys.argv[2]
	Subsample_fastq(fraction, inFolder)