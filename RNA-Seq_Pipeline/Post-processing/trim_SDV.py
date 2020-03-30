#!/usr/bin/env python
import pandas, sys, os

"""
Takes in an output folder of files from MDSeq where DV genes are ranked 
by padj from least to greatest and then outputs a trimmed file where 
there are no genes with padj > 0.05 in the same directory as the input

USAGE: trim_SDV.py <DeSeq_out_dirName>

Updated 180522 by Ronald Cutler
"""

def find_significant_cutoff(filename1, dirName):
	with open(dirName + filename1) as file1:
		filereader1 = pandas.read_csv(file1) 

	#iterating through padj column that is sorted from least to greatest
	header = list(filereader1)
	padj = header.index('FDR.dispersion')
	count = 0
	while filereader1.iloc[count, padj] < 0.050000000:
		count += 1

	if count == 0:
		print("No SDV Genes for above comparison!\n")
		return

	# extract the new table 
	data = filereader1[0 : (count)] # slicing the rows

	# make a new file that contains only SDE genes 
	with open(dirName + filename1 + "_SDV_only.csv", 'wt') as file2:
		data.to_csv(file2, index=False)


def runOnDirectory(dirName):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		if ('MDSeq') in fName:
			print('Running on file: ' + fName)
			find_significant_cutoff(fName, dirName)

if __name__ == "__main__":
	
	dirName = sys.argv[1]
	if (dirName[-1] != '/'):
		dirName += '/'
	runOnDirectory(dirName)

	