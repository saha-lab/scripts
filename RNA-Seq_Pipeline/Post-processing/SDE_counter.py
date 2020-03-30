#!/usr/bin/env python
import pandas, sys, os

"""
Takesa DESeq2 output file and gives how many SDE genes (< 0.05)
are upregulated and downregulated. This can be used on raw DESeq2
output csv files or trimmed SDE csv files

USAGE: SDE_counter.py <DeSeq_out_dirName>

Updated 180506 by Ronald Cutler
"""

def find_significant_cutoff(filename1, dirName):
	with open(dirName + filename1) as file1:
		filereader1 = pandas.read_csv(file1) 

	#iterating through padj column that is sorted from least to greatest
	header = list(filereader1)
	padj = header.index('padj')
	foldchange = header.index('log2FoldChange')

	up = 0
	down = 0

	for index, row in filereader1.iterrows():
		if row[padj] < 0.05000000:
			if row[foldchange] < 0:
				down += 1
			else:
				up += 1

	print("Upregulated =", up)
	print("Dowregulated =", down)

def runOnDirectory(dirName):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		if ('DESeq2') in fName:
			print('Running on file: ' + fName)
			find_significant_cutoff(fName, dirName)

if __name__ == "__main__":
	
	dirName = sys.argv[1]
	if (dirName[-1] != '/'):
		dirName += '/'
	runOnDirectory(dirName)