#!/usr/bin/env python

"""
Used to search KEGG IDs using gene names to provide to 
clusterProfiler for pathway enrichment. Takes a directory of
SDE trimmed DESeq2 otuput file. Uses the first 
column of an input csv for gene names and outputs a new 
csv with gene names in first column and KEGG IDs in the second.
This is made to be run on a DESeq2 output file with gene names in the first column.
Note that some KEGG IDs will not be found, due to lack of annotation.
This outputs a csv file with the gene names in the first column
and KEGG IDs in the second column.

This assumes that you have created a Kobas database to map KEGG IDs
to genes and it is in in tab-delimmeted file format with the gene names
in the first column and KEGG IDs in the second column

USAGE: gene_to_KEGG_ID.py <KOBAS_database.txt> <DESeq2_output_dir>

Updated 180518 by Ronald Cutler 
"""

import sys, pandas, os

def main(kobas, inFile, dirName):

	geneList = [] # genes to search
	found = [] # KEGG IDs found
	
	# get genes from csv 
	with open(dirName + inFile, 'r') as reader:
		geneCSVReader = pandas.read_csv(reader)
		geneList = list(geneCSVReader[geneCSVReader.columns[0]])

	# open KOBAS database and read gene-KEGG ID pairs into dict
	KEGG_dict = {}
	with open(kobas, 'r') as kobas_reader:
		for item in kobas_reader:
			if "#" in item:
				continue
			split = item.split('\t')
			if split[1].rstrip('\n') == "None":
				continue
			else:
				KEGG_dict[split[0]] = split[1].split('|')[0][4:]

	# search geneList against dictionary of gene-KEGG ID pairs
	not_found = 0
	for gene in geneList:
		try:
			found.append(KEGG_dict[gene])
		except KeyError:
			found.append('')
			not_found += 1

	print("Genes input = ", len(geneList))
	print("KEGG IDs Found = ", len(geneList) - not_found)

	# create dataframe, add columns, write csv
	df = pandas.DataFrame(columns = ["Gene", "KEGG_ID"])
	df["Gene"] = geneList
	df["KEGG_ID"] = found
	df.to_csv(dirName + inFile[:-4] + "_KEGG_IDs.csv", index = False)

def runOnDirectory(kobas, dirName):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		if ('DESeq2' in fName) or ('MDSeq' in fName):
			print ('Running on file: ' + fName)
			main(kobas, fName, dirName)

if __name__ == "__main__":
	dirName = sys.argv[2]
	if (dirName[-1] != '/'):
		dirName += '/'
	runOnDirectory(sys.argv[1], dirName)