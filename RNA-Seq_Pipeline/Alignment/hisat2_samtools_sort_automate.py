#!/usr/bin/env python
"""
This assumes that the hisat version being used is at least hisat 2.1.0 which makes use of the --summary-file argument

Runs hisat2, samtools view, and samtools sort on a directory containing paired-end fastq files that are 
in their respective sample folders. Given an input directory, this will recursively go through each folder 
to identify the paired-end reads belonging to each sample and align these using hisat2. This will then create 
an alignment directory that is specified where the output all of the alignment files and their respective 
log files will be placed.

INPUT: inputDirectory, indexFolder, hisat2 parameters, samtools sort parameter, outFolder
OUTPUT: log file, sorted alignment bam file with replicate number in path of outFolder

See the benchling protocol 'RNA-Seq read alignment' for an example on how to run this. 

IMPORTANT DISCLAIMER: This DOES NOT WORK with samples that have been run
over multiple lanes! This script only works for data that is paired-ended,
with one forward and one reverse file for each sample. Merge these fastq files beforerhand!

Also, make sure the directory that the fastq files are in has no spaces. Use underscores instead.

Written by Ronald Cutler & Caroline Golino
Updated 180505 by Ronald CUtler 
"""

import os, sys, subprocess
from glob import glob

def RunHisat2(indexFolder, inFiles, outFolder, threads, orient, options, sort):
	"""Given a list of fastq files, run hisat2 on these paired end reads"""

	for v, w in zip(inFiles[::2], inFiles[1::2]):
		in1 = v  
		in2 = w

		print ("\nRunning hisat2...")
		print ("Read 1:", v)
		print ("Read 2:", w)
		
		# slicing out mate 1 name for output.bam name
		in1_new = slice(in1)
		print ("\nOutput bam file:", in1_new)

		# printing hisat2 command and then running hisat2
		print('\nCMD: hisat2 {0} -p {1} --rna-strandness {2} --summary-file {7}{8}_hisat2_output_log.txt -x {3} -1 {4} -2 {5} | samtools view -@ {1} -Shu - | samtools sort - -@ {1} {6} > {7}{8}_hisat2_output.bam'.format(options, threads, orient, indexFolder, in1, in2, sort, outFolder, in1_new))
		os.system('hisat2 {0} -p {1} --rna-strandness {2} --summary-file {7}{8}_hisat2_output_log.txt -x {3} -1 {4} -2 {5} | samtools view -@ {1} -Shu - | samtools sort - -@ {1} {6} > {7}{8}_hisat2_output.bam'.format(options, threads, orient, indexFolder, in1, in2, sort, outFolder, in1_new))
		print ('\nDone Mapping, Sorting, & Compressing:\n {0} \n {1}\n'.format(in1, in2))

def slice(str):
	"""cuts out the path and and only returns the sample name"""
	new_string = ''
	for i in reversed(str): #reading in str reversed
   		if i != '/': #stopping building once we hit '/'
   			new_string += i
   		else:
   			new_string = new_string[::-1] #re-reversing
   			if new_string.endswith('.fastq.gz'):
   				new_string = new_string[:-9]
   			if new_string.endswith('.fastq'): 
   				new_string = new_string[:-6] #cutting out .fastq
   			return new_string


def getInput():
	"""Gets input from user on what options, files and directories to use"""
	userInput = [] # path, index, threads, sort, orient, options, outputDir

	path = input('Path to the folder containing the .fastq.gz or fq.gz files (paired-end) you wish to align?\n').rstrip(' ')
	userInput.append(path)

	userInput.append(input('Path to the index files (just the basename) you would like to use?\n').rstrip(' '))

	threads = input("How many threads would you like to use?\n")
	while( 1 < int(threads) < 24 ):
		threads = input("Please enter an integer between 1-24\n")
	userInput.append(threads)

	sort = input("How would you like to sort the alignment file: name or coord\n").rstrip(' ')
	if sort == "name":
		userInput.append("-n")
	elif sort == "coord":
		userInput.append('')

	orient = input("What is the orientation of the paired-end reads? Enter FR or RF\n").rstrip(' ')
	if orient == "RF" or orient == "FR":
		userInput.append(orient)

	userInput.append(input("What other option would you like to use with hisat2? Input them here as if you were running the program manually\n"))

	path = input('What is the path to the output folder you would like to create?\n').rstrip(' ')
	if (path[-1] != '/'):
		path+='/'
	userInput.append(path)

	return userInput

def main( ):
	userInput = getInput()

	fastqfiles = [y for x in os.walk(userInput[0]) for y in glob(os.path.join(x[0], '*.fastq.gz'))]
	if len(fastqfiles) <= 0:
		fastqfiles = [y for x in os.walk(userInput[0]) for y in glob(os.path.join(x[0], '*.fq.gz'))]

	print ("\nList of", len(fastqfiles), "files being run through...")

	for file in fastqfiles:
		print(file)

	print ("\nIndex Folder:", userInput[1], "\n")
	# create the directory 
	try:
		os.makedirs(userInput[6])
		print("\nOutput Folder:", userInput[6], "\n")
	except FileExistsError:
		print("The output folder:", userInput[6], "already exist! Provide a path to a folder that does not exist.\n")
		sys.exit()

	# run hisat2
	RunHisat2(userInput[1], fastqfiles, userInput[6], userInput[2], userInput[4], userInput[5], userInput[3])


if __name__ == "__main__":
	main( )



