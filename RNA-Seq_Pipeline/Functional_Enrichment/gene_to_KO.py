#!/usr/bin/env python
"""
This is for converting gene names into KO IDs to perform KEGG enrichment
or over-representation analysis using clusterProfiler.
Given a csv file with genes in the first column with the header 'Gene', 
find the KO ID number in another txt file where the genes names and 
KO numbers are separated by a tab.
Since all the genes are unable to be annotated, some do not have 
corresponding KO IDs. These are left out and output into another 
file for reference.
This outputs a csv file with the gene names in the first column
and KO IDs in the second column.

USAGE: gene_to_KO.py <KO_database.txt> <gene.csv>

Updated by Ronald Cutler 180108
"""

import sys, pandas

def main(knums, genes):

	geneList = [] # genes to search
	found = [] # KO IDs found

	# Get genes from csv
	with open(genes, 'r') as reader:
		geneCSVReader = pandas.read_csv(reader)
		geneList = list(geneCSVReader[geneCSVReader.columns[0]])

	# remove pseudogenes from list
	# either ".Sp" or ".Lp"
	for gene in geneList:
		split = gene.split("|")
		if split[0][-2:] == "Sp" or split[0][-2:] == "Lp" or split[0][-2:] == "0p" or split[0][-2:] == "1p" \
		or split[0][-2:] == "6p" or split[0][-2:] == "5p" or split[0][-2:] == "9p" or split[0][-2:] == "2p" \
		or split[0][-2:] == "4p" or split[0] == "LOC100497309.Sp" or split[0] == "slc25a32.Sp":
			geneList.remove(gene)

	# open KO database and read gene-KO pairs into dict
	KO_dict = {}
	with open(knums, 'r') as knum_reader:
		for item in knum_reader:
			split = item.split('\t')
			if len(split) == 2:
				KO_dict[split[0]] = split[1].rstrip('\n')

	# search geneList against dictionary of gene-KO pairs
	not_found = 0
	for gene in geneList:
		try:
			found.append(KO_dict[gene])
		except KeyError:
			found.append('')
			not_found += 1

	print("Genes input = ", len(geneList))
	print("KO IDs Found = ", len(geneList) - not_found)

	# create dataframe, add columns, write csv
	df = pandas.DataFrame(columns = ['Gene', 'KO'])
	df['Gene'] = geneList
	df['KO'] = found
	df.to_csv(genes[:-4] + "_KO_IDs.csv", index = False)


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])