
#!/usr/bin/env python
"""

Runs gsnap on a directory containing paired-end fastq files that are 
in their respective sample folders. Given an input directory, this will recursively go through each folder 
to identify the paired-end reads belonging to each sample and align these using gsnap. This will then create 
an alignment directory that is specified where the output all of the alignment files and their respective 
log files will be placed.

INPUT: gsnap database, inputDirectory, gsnap parameters, outFolder
OUTPUT: sorted alignment sam file with replicate number in path of outFolder

See the benchling protocol 'GSNAP RNA-Seq read alignment' for an example on how to run this. 

IMPORTANT DISCLAIMER: This DOES NOT WORK with samples that have been run
over multiple lanes! This script only works for data that is paired-ended,
with one forward and one reverse file for each sample. Merge these fastq files beforerhand!

Also, make sure the directory that the fastq files are in has no spaces. Use underscores instead.

Written by Grace Solini (190614)
Adapted from hisat2_samtools_sort_automate.py - written by Ronald Cutler and Caroline Golino
"""

import os, sys, subprocess
from glob import glob


def RunGSNAP(database, inFiles, outFolder, threads, orient, options, novel_splicing, output_type):
	"""Given a list of fastq files, run gsnap on these paired end reads"""

	for v, w in zip(inFiles[::2], inFiles[1::2]):
		in1 = v  
		in2 = w

		print ("\nRunning gsnap...")
		print ("Read 1:", v)
		print ("Read 2:", w)
		
		# slicing out mate 1 name for output.sam name
		in1_new = slice(in1)
		print ("\nOutput sam file:", in1_new)

		#splitting database into its path and sample name (required for gsnap run)
		database_name = slice(database)
		database_path = sliceRev(database)

		# printing gsnap command and then running gsnap
		print('\nCMD: gsnap --gunzip -D {0} -d {1} --orientation={2} -A {3} -t {4} -N {5} {6} {7} {8} > {9}{10}_gsnap_output.sam'.format(database_path, database_name, orient, output_type, threads, novel_splicing, options, in1, in2, outFolder, in1_new))
		os.system('gsnap --gunzip -D {0} -d {1} --orientation={2} -A {3} -t {4} -N {5} {6} {7} {8} > {9}{10}_gsnap_output.sam'.format(database_path, database_name, orient, output_type, threads, novel_splicing, options, in1, in2, outFolder, in1_new))
		print ('\nDone Mapping:\n {0} \n {1}\n'.format(in1, in2))

def slice(str):
	"""cuts out the path and only returns the sample name"""
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

def sliceRev(string):
 	"""cuts out the sample name and returns only the path to it"""
 	new_string = string.rstrip(slice(string))

 
 	return new_string

def getInput():
	"""Gets input from user on what options, files and directories to use"""
	userInput = [] # path, databse, threads, orient, options, outputDir

	path = raw_input('Path to the folder containing the .fastq.gz or fq.gz files (paired-end) you wish to align?\n').rstrip(' ')
	userInput.append(path)

	userInput.append(raw_input('Path to the the database you would like to use is in?\n').rstrip(' '))

	threads = raw_input("How many threads would you like to use?\n")
	while( 1 > int(threads) or 64 < int(threads)):
		threads = raw_input("Please enter an integer between 1-64\n")
	userInput.append(threads)

	orient = raw_input("What is the orientation of the paired-end reads? Enter FR or RF\n").rstrip(' ')
	if orient == "RF" or orient == "FR":
		userInput.append(orient)

	userInput.append(raw_input("What other option would you like to use with gsnap? Input them here as if you were running the program manually\n"))

	path = raw_input('What is the path to the output folder you would like to create? Please be sure this folder does not already exist or it will get overwrited!\n').rstrip(' ')
	if (path[-1] != '/'):
		path+='/'
	userInput.append(path)

	return userInput

def main( ):
	userInput = getInput()

	fastqfiles = [y for x in os.walk(userInput[0]) for y in glob(os.path.join(x[0], '*.fastq.gz'))]
	fastqfiles = sorted(fastqfiles)
	if len(fastqfiles) <= 0:
		fastqfiles = [y for x in os.walk(userInput[0]) for y in glob(os.path.join(x[0], '*.fq.gz'))]
		fastqfiles = sorted(fastqfiles)
	print ("\nList of", len(fastqfiles), "files being run through...")

	for file in fastqfiles:
		print(file)

	print ("\nIndex Folder:", userInput[1], "\n")
	# create the directory 
	#try:
	os.makedirs(userInput[5])
	print("\nOuput Folder:", userInput[5], "\n")
	"""FileExistsError does not exist in python 2.7.5, which is what the hpc uses - so I have had to remove this part of the code"""
	#except FileExistsError:
	#	print("The output folder:", userInput[6], "already exists! Provide a path to a folder that does not exist.\n")
	#	sys.exit()

	#always turn novel splicing on
	novel_splicing = 1

	#always set output type to .sam
	output_type = 'sam'

	#run GSNAP
	RunGSNAP(userInput[1], fastqfiles, userInput[5], userInput[2], userInput[3], userInput[4], novel_splicing, output_type)


if __name__ == "__main__":
	main( )



