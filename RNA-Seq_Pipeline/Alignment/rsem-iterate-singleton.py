#!/usr/bin/env python
"""
Runs RSEM using bowtie2 alignment to transcriptome index with reverse stranded single-end reads 

INPUT: indexFolder, inFiles, outFolder
OUTPUT: bam files with replicate number in path of outFolder 

IMPORTANT DISCLAIMER: This DOES NOT WORK with samples that have been run
over multiple lanes! This script only works for data that is paired-ended,
with one forward and one reverse file for each sample.

Updated 170522 by Ronald Cutler
"""
import os, sys

def RunSalmon(indexFolder, inFiles, outFolder):
	filenames = [os.path.join(root, name)
         for root, dirs, files in os.walk(inFiles)
         for name in files
         if ".fastq" in name]
	
	print("Index Folder:", indexFolder)
	print("Output Folder:", outFolder)
	print('Files being ran through script...\n')

	for files in filenames:
		print(files)

	for singleton in filenames:

		in1 = singleton  
		print("Mate 1 is", in1)
		
		#slicing out mate 1 name for output.bam name
		in1_new = slice(in1)
		print("Output Sample Folder:", outFolder + in1_new)

		# Run on 24 threads assuming each paired end is contained in their respective file
		os.system("rsem-calculate-expression --bowtie2 -p 24 --append-names --strandedness reverse {0} {1} {2}/{3}".format(in1, indexFolder, outFolder, in1_new))
		print('Done Mapping & Compressing {0}\n'.format(in1))

#cuts out the path and and only returns the sample name
def slice(str):
 	new_string = ''
   	for i in reversed(str): #reading in str reversed
   		if i != '/': #stopping building once we hit '/'
   			new_string += i
   		else:
   			new_string = new_string[::-1] #re-reversing
   			if new_string.endswith('.fastq.gz'):
   				new_string = new_string.rstrip('.fastq.gz')
   			if new_string.endswith('.fastq'): 
   				new_string = new_string.rstrip('.fastq') #cutting out .fastq
			return new_string


def getInput():
	# Gets input from user on what options, files and directories to use
	userInput = []

	path = raw_input('What is the folder containing the .fastq files you wish to align?\n')
	userInput.append(path)

	userInput.append(raw_input('Where is the index file you would like to use (base name)?\n'))

	path = raw_input('Where would you like to ouput your files?\n')
	userInput.append(path)

	return userInput



if __name__ == "__main__":

	userInput = getInput()
	print()

	RunSalmon(userInput[1], userInput[0], userInput[2])

