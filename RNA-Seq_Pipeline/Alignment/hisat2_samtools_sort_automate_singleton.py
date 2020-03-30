#!/usr/bin/env python
"""
Runs hisat2, samtools view, and samtools sort in a folder containing pairs of files that are paired-end reads. 

INPUT: hisat2_samtools_sort_automate_singleton.py
OUTPUT: sorted bam files with replicate number in path of outFolder 

IMPORTANT DISCLAIMER: This script only works for data that is single-ended.
Paired-end reads should use the other hisat2 automated script.

Also, make sure the directory that the fastq files are in has no spaces.
Use underscores instead.

Based on paired-end script by Ronald Cutler & Caroline Golino
Written by LeAnn Lo 180210
"""
import os, sys

def RunHisat2(indexFolder, inFiles, outFolder, threads, options, sort):
	fastqfiles = [os.path.join(root, name)
	             for root, dirs, files in os.walk(inFiles)
	             for name in files]

	print "Index file:", indexFolder
	print "Output Folder:", outFolder
	print 'Files being ran through script...'
	for files in fastqfiles:
		print files
	print "\n"

	for v in fastqfiles:
		in1 = v  
		print "Quantifying:", in1
		
		#slicing out mate 1 name for output name
		in1_new = slice(in1)
		print("Output Sample Folder: " + outFolder + in1_new)

		# Run on 24 threads assuming each paired end is contained in their respective file
		os.system('hisat2 {0} -p {1} -x {2} -U {3} | samtools view -@ {1} -Sb - | samtools sort - -@ {1} {4} > {5}/{6}_hisat2_output.bam'.format(options, threads, indexFolder, in1, sort, outFolder, in1_new))
		print 'Done Quantifying', in1

#cuts out the path and and only returns the sample name
def slice(str):
 	new_string = ''
   	for i in reversed(str): #reading in str reversed
   		if i != '/': #stopping building once we hit '/'
   			new_string += i
   		else:
   			new_string = new_string[::-1] #re-reversing
   			if new_string.endswith('.bam_sorted.bam'):
   				new_string = new_string.rstrip('.bam_sorted.bam')
   			if new_string.endswith('.bam'): 
   				new_string = new_string.rstrip('.bam') #cutting out .bam
			return new_string


def getInput():
	# Gets input from user on what options, files and directories to use
	userInput = []

	path = raw_input('Path to the folder containing the .fastq files (single-ended) you wish to align?\n')
	userInput.append(path)

	userInput.append(raw_input('Path to the index files (just the basename) you would like to use?\n'))

	threads = raw_input("How many threads would you like to use?\n")
	while( 1 <= threads < 24 ):
		threads = raw_input("Please enter an integer between 1-24\n")
	userInput.append(threads)

	sort = raw_input("How would you like to sort the alignment file: name or coord\n")
	if sort == "name":
		userInput.append("-n")
	elif sort == "coord":
		userInput.append('')
	else:
		sort = raw_input("Please choose either name or coord\n")

	userInput.append(raw_input("What other option would you like to use with hisat2? Input them here as if you were running the program manually\n"))

	path = raw_input('What is the path to the output folder?\n')
	if (path[-1] != '/'):
		path+='/'
	userInput.append(path)

	return userInput


if __name__ == "__main__":

	userInput = getInput()
	print

	RunHisat2(userInput[1], userInput[0], userInput[5], userInput[2], userInput[4], userInput[3])


