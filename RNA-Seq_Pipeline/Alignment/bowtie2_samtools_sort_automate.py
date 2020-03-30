#!/usr/bin/env /usr/local/Cellar/python@2/2.7.14_1/bin/python2
"""
Runs bowtie2, samtools view, and samtools sort in a folder containing pairs of files that are paired-end reads. 

INPUT: indexFolder, inFiles, outFolder
OUTPUT: sorted bam files with replicate number in path of outFolder 

IMPORTANT DISCLAIMER: This DOES NOT WORK with samples that have been run
over multiple lanes! This script only works for data that is paired-ended,
with one forward and one reverse file for each sample. Please merge the files 
using samtools merge beforehand.

Also, make sure the directory that the fastq files are in has no spaces.
Use underscores instead.

Updated by Ronald Cutler 180306
"""

import os, sys

def RunBowtie2(indexFolder, inFiles, outFolder, threads, options, sort):
	"""Given a list of fastq files, run hisat2 on these paired end reads"""

	for v, w in zip(inFiles[::2], inFiles[1::2]):
		in1 = v  
		in2 = w

		print ("\nRunning bowtie2...")
		print ("Mate 1:", v)
		print ("Mate 2:", w)
		
		#slicing out mate 1 name for output.bam name
		in1_new = slice(in1)
		print ("\nOutput bam file:", in1_new)

		# Run on 24 threads assuming each paired end is contained in their respective file
		os.system('bowtie2 {0} -p {1} -x {2} -1 {3} -2 {4} | samtools view -@ {1} -Sb - | samtools sort - -@ {1} {5} > {6}/{7}_bowtie2_output.bam'.format(options, threads, indexFolder, in1, in2, sort, outFolder, in1_new))
		print ('Done Mapping, Sorting, & Compressing {0} & {1}\n'.format(in1, in2))


#cuts out the path and and only returns the sample name
def slice(str):
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
	# Gets input from user on what options, files and directories to use
	userInput = [] # path, index, threads, sort, options, outputDir

	path = raw_input('Path to the folder containing the .fastq files (paired-end) you wish to align?\n')
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

	userInput.append(raw_input("What other option would you like to use with bowtie2? Input them here as if you were running the program manually\n"))

	path = raw_input('What is the path to the output folder?\n')
	if (path[-1] != '/'):
		path+='/'
	userInput.append(path)

	return userInput

def main( ):
	userInput = getInput()

	print ("\nIndex Folder:", userInput[1])

	if not os.path.exists(userInput[5]):
		print ("Error, please provide a correct output path")
		sys.exit()
	else:
		print ("\nOutput Folder:", userInput[5])

	print ("List of files being run through...")
	print (userInput[0])
	fastqfiles= []
	for file in os.listdir(userInput[0]):
		if ".fastq.gz" in file:
			fastqfiles.append(os.path.join(userInput[0], file))

	for file in fastqfiles:
		print (file)

	RunBowtie2(userInput[1], fastqfiles, userInput[5], userInput[2], userInput[4], userInput[3])


if __name__ == "__main__":
	main( )



