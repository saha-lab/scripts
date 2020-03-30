#!/usr/bin/env python

"""
Using the Taeniopygia_guttata.taeGut3.2.4.92_mapping.csv mapping file 
to insert extra columns into DESEq2 output csv to provide information
on gene symbol, gene description, and chromosome location.
It is expected that the first column have the ensemble gene ID i.e. ENSTGUGxxx

Last updated 170517 by Ronald Cutler

USAGE: zebra_finch_annotation_mapper.py <Taeniopygia_guttata.taeGut3.2.4.92_mapping.csv> <DESeq2_output.csv>
"""
import sys, pandas

def main(in_map, in_file):
	# create a dictionary out of the mapping file
	# e.g. 'ENSTGUG00000017489': ['ALPK2', 'Alpha-protein kinase 2 (EC 2.7.11.-)(Heart alpha-protein kinase) [Taeniopygia guttata]', 'Z_random']
	geneMapDict = {}
	with open(in_map) as geneMap:
		for line in geneMap:
			lineSplit = line.split(',')
			lineSplit[4] = lineSplit[4].rstrip('\n') # remove newline from chromosome names
			geneMapDict[lineSplit[0]] = lineSplit[2:5]

	# read in deseq2 output csv
	with open(in_file) as file1:
		geneCSVReader = pandas.read_csv(file1)

	# get first column
	geneList = geneCSVReader[geneCSVReader.columns[0]]

	# holding corresponding information
	symbolList = []
	descripList = []
	chromList = []

	# iterate through the first column of the deseq2 output csv and assign descriptions 
	for item in geneList:
		info = geneMapDict.get(item)
		if info != None:
			symbolList.append(info[0])
			descripList.append(info[1])
			chromList.append(info[2])
		else:
			symbolList.append('NA')
			descripList.append('NA')
			chromList.append('NA')
			

	# add the columns to the data frame 
	geneCSVReader = geneCSVReader.assign(Symbol = symbolList)
	geneCSVReader = geneCSVReader.assign(Description = descripList)
	geneCSVReader = geneCSVReader.assign(Chromosome = chromList)

	# reordering columns from the back to the front
	cols = geneCSVReader.columns.tolist()
	cols = cols[:-3] # remove the last 3 columns
	cols.insert(1, 'Chromosome')
	cols.insert(1, 'Description')
	cols.insert(1, 'Symbol')
	geneCSVReader = geneCSVReader[cols]

	# overwrite input csv
	with open(in_file, 'wt') as fileOut:
		geneCSVReader.to_csv(fileOut, index = False)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])

