#!/usr/bin/env python
"""
Given a text file with gene names on each lines,
edit a csv outptut by DESeq with gene names in the first column
and that this column is named 'Gene', remove rows that contain the 
gene names in the input text file.

USAGE: filter_DESeq_csv <gene_names.txt> <DEseq_results.csv>

Updated 170904 by Ronald Cutler
"""

import csv, pandas, sys, os

def main(geneList, inCSV):
	to_remove = []
	with open( geneList, 'r') as geneReader:
		for line in geneReader:
			to_remove.append(line.rstrip('\n'))

	with open(inCSV) as file1:
		geneCSVReader = pandas.read_csv(file1)

	geneList = geneCSVReader['Gene']
	count = 0

	# iterating through dataframe and removing rows
	for item in geneList:
		if item in to_remove:
			geneCSVReader = geneCSVReader[geneCSVReader.gene != item]
			count += 1

	with open(inCSV[:-3] + "_new.csv", 'wt') as fileOut:
		geneCSVReader.to_csv(fileOut, index = False)

	print("Removed", count, "genes")

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])