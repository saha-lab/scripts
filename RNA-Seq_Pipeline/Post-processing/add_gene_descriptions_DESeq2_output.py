#!/usr/bin/env python
"""
Add a gene descriptions column to the DESEq2 output csv
The current mappng file used for uncollapsed X. laevis gene names is 
loacted at: /Volumes/cachannel/RNA_SEQ/Analysis/Reference/X_laevis/9.1_Reference_Files/Functional_annotation/XenopusLaevis_GeneID_Description.txt

Input: <gene_description_mapping_file> <dir_name> [output folder]
Note the output folder argument is optional

Updated 180506 by Ronald Cutler
"""
import csv, pandas, sys, os

def main(inMap, gene_csvIn, dirName, outName):
	# create a dictionary out of the mapping file
	geneMapDict = {}
	with open(inMap, 'r') as geneMap:
		for line in geneMap:
			lineSplit = line.split('\t')
			geneMapDict[lineSplit[0]] = lineSplit[1].rstrip('\n')

	with open(dirName + gene_csvIn) as file1:
		geneCSVReader = pandas.read_csv(file1)

	# iterate through the first column of the csv and assign descriptions 
	geneList = geneCSVReader[geneCSVReader.columns[0]]
	descripList = []

	for item in geneList:
		descrip = geneMapDict.get(item)
		if descrip != None:
			descripList.append(descrip)
		else:
			descripList.append('NA')

	# add the column to the data frame 
	geneCSVReader = geneCSVReader.assign(name = descripList)

	# reordering 
	cols = geneCSVReader.columns.tolist()
	cols = cols[:-1]
	cols.insert(1, 'name')
	geneCSVReader = geneCSVReader[cols]

	# write new dataframe
	with open(outName + gene_csvIn, 'wt') as fileOut:
		geneCSVReader.to_csv(fileOut, index = False)

def runOnDir(inMap, dirName, outName):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		if fName.endswith('.csv'):
			print("Running on file:"),  fName
			main(inMap, fName, dirName, outName)

if __name__ == "__main__":
	dirName = sys.argv[2]
	if (dirName[-1] != '/'):
		dirName += '/'

	try:
		outName = sys.argv[3]
		if (outName[-1] != '/'):
			outName += '/'
	except IndexError:	
		outName = dirName
		
	
	runOnDir(sys.argv[1], dirName, outName)