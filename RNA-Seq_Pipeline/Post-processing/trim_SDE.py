#!/usr/bin/env python
import pandas, sys, os

"""
Takes in an output folder of files from DESeq where genes are ranked 
by padj from least to greatest and then outputs a trimmed file where 
there are no genes with padj > 0.05 in the same directory as the input

USAGE: trim_SDE.py <DeSeq_out_dirName>

Updated 180506 by Ronald Cutler
"""

def find_significant_cutoff(filename1, dirName):
	with open(dirName + filename1) as file1:
		filereader1 = pandas.read_csv(file1) 

	#iterating through padj column that is sorted from least to greatest
	header = list(filereader1)
	padj = header.index('padj')
	count = 0
	try:
		bol = filereader1.iloc[count, padj] < 0.05000000
	except IndexError:
		print("Check File")

	while bol:
		#print(filereader1.iloc[count, padj])
		count += 1
		try:
			bol = filereader1.iloc[count, padj] < 0.05000000
		except IndexError:
			break
			
		if count == 0:
			print("No SDE Genes for above comparison!\n")
			return

	# extract the new table 
	data = filereader1[0 : (count)] # slicing the rows

	# make a new file that contains only SDE genes 
	with open(dirName + filename1 + "_SDE_only.csv", 'wt') as file2:
		data.to_csv(file2, index=False)


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

	