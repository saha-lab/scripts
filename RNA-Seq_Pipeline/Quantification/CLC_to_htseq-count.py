#!/usr/bin/env python
"""
Script to convert the results of CLC RNA-Seq alignment and quantification output in csv format and convert
these files to HTSeq-count format text files for input into DESeq2. This will run on a directory of exported
CLC csv files and produce new HTSeq-count txt files with the same names as the csv files. 

Note that this retrieves the gene names and the unique counts from the CLC output file. This was also designed
to split the read counts into two files, for bacterial and phage counts, where phage genes were identified by 
when the gene name conatins 'Gene'

USAGE: CLC_to_htseq-count.py <in_directory>

Update 180628 by Ronald Cutler
"""

import sys, os
import pandas as pd

def main(fName, dirName):
	# open the csv
	with open(dirName + fName, 'r') as file1:
		filereader = pd.read_csv(file1)

	# get the gene and unique counts columns
	genes = list(filereader['Name'])
	counts = list(filereader['Unique gene reads'])

	# output HTSeq-count format text file for bacteria and phage
	with open(dirName + fName[:-4] + "_bacteria.txt", 'w') as file2:
		with open(dirName + fName[:-4] + "_phage.txt", 'w') as file3:
			for gene, count in zip(genes, counts):
				# splitting file if the gene name continas 'Gene' meaning it is from the phage
				if 'Gene' in gene:
					file3.write(gene + "\t" + str(count) + "\n")
				else:
					file2.write(gene + "\t" + str(count) + "\n")


	"""
	# output HTSeq-count format text file for combined bacteria and phage
	with open(dirName + fName[:-4] + "_combined.txt", 'w') as file2:
		for gene, count in zip(genes, counts):
			file2.write(gene + "\t" + str(count) + "\n")
	"""
def runOnDirectory(dirName):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		if ('.csv') in fName:
			print('Running on file: ' + fName)
			main(fName, dirName)

if __name__ in "__main__":

	dirName = sys.argv[1]
	if dirName[:-1] != '/':
		dirName = dirName + '/'

	runOnDirectory(dirName)
