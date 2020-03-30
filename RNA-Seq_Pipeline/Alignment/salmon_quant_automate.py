#!/usr/bin/env python
# Note that this is only compatible with python3

"""
Runs salmon quant over all paired-end read files in the provided input folder.

INPUT: indexFolder, inFiles, outFolder
OUTPUT: bam files with replicate number in path of outFolder 

fastq reads must be gzipped

IMPORTANT DISCLAIMER: This DOES NOT WORK with samples that have been run
over multiple lanes! This script only works for data that is paired-ended,
with one forward and one reverse file for each sample.

Updated 180305 by Ronald Cutler
"""
import os, sys
from glob import glob

def RunSalmon(indexFolder, inFiles, outFolder, options):
	print("Index Folder:", indexFolder)
	print("Output Folder:", outFolder)
	print('Files being run through script...\n')

	filenames = [y for x in os.walk(inFiles) for y in glob(os.path.join(x[0], '*fastq.gz'))]
	for file in filenames:
		print (file)
	print()

	for v, w in zip(filenames[::2], filenames[1::2]):
		in1 = v  
		in2 = w

		print("Mate 1 is", v)
		print("Mate 2 is", w)
		
		#slicing out mate 1 name for output.bam name
		in1_new = slice(in1)
		print("Output Sample Folder:", outFolder + in1_new, "\n")

		# Run on 24 threads assuming each paired end is contained in their respective file
		os.system('salmon quant {0} --index {1} -1 {2} -2 {3} -o {4}/{5}'.format(options, indexFolder, in1, in2, outFolder, in1_new))
		print('Done Mapping & Compressing {0} & {1}\n'.format(in1, in2))

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
	userInput = []# [input, index, options, outputDir]
	path = input('What is the folder containing the .fastq files you wish to align?\n')
	userInput.append(path)

	userInput.append(input('Where is the index file you would like to use?\n'))

	userInput.append(input('What other options would you like to use? Input them as you would normally.\n'))

	path = input('Where would you like to ouput your files?\n')
	userInput.append(path)

	return userInput



if __name__ == "__main__":

	userInput = getInput()
	print()

	RunSalmon(userInput[1], userInput[0], userInput[3], userInput[2])


