#!/usr/bin/env python
"""
This script runs on a whole directory of shared_finder_two.py outputs and outs a corresponding file for each
on what are the genes that are shared that have different foldchanges in the two comparisons they orgininated from.

IMPORTANT: YOU NEED TO MAKE SURE THAT THE COMPARISONS WERE MADE IN THE SAME DIRECTION
e.g. Control vs Experimental1 & Control vs Experimental2

USAGE: shared_gene_FC_diff.py <input_dir>

Updated 170909 by Ronald Cutler 
"""

import sys, os, numpy, argparse 
import pandas as pd

def get_shared(inCSV, inDir):
	with open(inDir + inCSV) as file1:
		geneCSVReader = pd.read_csv(file1)

	geneList = geneCSVReader['shared_genes'].tolist()
	foldChange = geneCSVReader['log2FoldChange'].tolist()
	rank = geneCSVReader['parent_rank'].tolist()
	parent_list = geneCSVReader['parent_list'].tolist()
	padj = geneCSVReader['padj'].tolist()

	output_list = [geneList, foldChange, rank, parent_list, padj]
	return output_list

def compare_shared(geneList, foldChange, rank, parent_list, padj):

	# since the shared genes are every two entries, split these list
	geneList_1 = []
	foldChange_1 = []
	rank_1 = []
	parent_list_1 = []
	padj_1 = []

	geneList_2 = []
	foldChange_2 = []
	rank_2 = []
	parent_list_2 = []
	padj_2 = []

	parent_list_1 = parent_list[0]
	parent_list_2 = parent_list[1]

	count = 0
	while count < len(geneList):
		if(((count + 1) % 2) != 0):
			geneList_1.append(geneList[count])
			foldChange_1.append(foldChange[count])
			rank_1.append(rank[count])
			padj_1.append(padj[count])
		else:
			geneList_2.append(geneList[count])
			foldChange_2.append(foldChange[count])
			rank_2.append(rank[count])
			padj_2.append(padj[count])

		count += 1 
	# length of list should be equal 
	if len(geneList_1) != len(geneList_2):
		print "Length of gene list differ! Exiting..."
		sys.exit()

	# comparing the fold changes 
	geneList_1_diff = []
	foldChange_1_diff = []
	rank_1_diff = []
	#parent_list_1_diff = []
	padj_1_diff = []

	geneList_2_diff = []
	foldChange_2_diff = []
	rank_2_diff = []
	#parent_list_2_diff = []
	padj_2_diff = []

	count = 0
	while count < len(geneList_1):
		if (foldChange_1[count] < 0) and (foldChange_2[count] > 0):
			geneList_1_diff.append(geneList_1[count])
			foldChange_1_diff.append(foldChange_1[count])
			rank_1_diff.append(rank_1[count])
			#parent_list_1_diff.append(parent_list_1[count])
			padj_1_diff.append(padj_1[count])

			geneList_2_diff.append(geneList_2[count])
			foldChange_2_diff.append(foldChange_2[count])
			rank_2_diff.append(rank_2[count])
			#parent_list_2_diff.append(parent_list_1[count])
			padj_2_diff.append(padj_2[count])

		elif (foldChange_1[count] > 0) and (foldChange_2[count] < 0):
			geneList_1_diff.append(geneList_1[count])
			foldChange_1_diff.append(foldChange_1[count])
			rank_1_diff.append(rank_1[count])
			#parent_list_1_diff.append(parent_list_1[count])
			padj_1_diff.append(padj_1[count])

			geneList_2_diff.append(geneList_2[count])
			foldChange_2_diff.append(foldChange_2[count])
			rank_2_diff.append(rank_2[count])
			#parent_list_2_diff.append(parent_list_1[count])
			padj_2_diff.append(padj_2[count])

		count += 1

	# length of list should be equal 
	if len(geneList_1_diff) != len(geneList_2_diff):
		print "Length of gene list differ! Exiting..."
		sys.exit()

	elif len(geneList_1_diff) == 0:
		print "No differentially FC Genes"
		dataframe = pd.DataFrame({ parent_list_1 : geneList_1_diff, parent_list_2 : geneList_2_diff, 'logFoldChange_1' : foldChange_1_diff, 'logFoldChange_2' : foldChange_2_diff, 'Rank_1' : rank_1_diff, 'Rank_2' : rank_2_diff, 'padj_1' : padj_1_diff, 'padj_2' : padj_2_diff})
	else:

		geneList_1_diff = numpy.array(geneList_1_diff)
		foldChange_1_diff = numpy.array(foldChange_1_diff)
		rank_1_diff = numpy.array(rank_1_diff)
		padj_1_diff = numpy.array(padj_1_diff)

		geneList_2_diff = numpy.array(geneList_2_diff)
		foldChange_2_diff = numpy.array(foldChange_2_diff)
		rank_2_diff = numpy.array(rank_2_diff)
		padj_2_diff = numpy.array(padj_2_diff)



		dataframe = pd.DataFrame({ parent_list_1 : geneList_1_diff, parent_list_2 : geneList_2_diff, 'logFoldChange_1' : foldChange_1_diff, 'logFoldChange_2' : foldChange_2_diff, 'Rank_1' : rank_1_diff, 'Rank_2' : rank_2_diff, 'padj_1' : padj_1_diff, 'padj_2' : padj_2_diff})
		cols = dataframe.columns.tolist()
		cols = [parent_list_1, parent_list_2, 'logFoldChange_1', 'logFoldChange_2', 'Rank_1', 'Rank_2', 'padj_1', 'padj_2']
		dataframe = dataframe[cols]

		print "FOUND", len(geneList_1_diff), "DIFF FC SHARED GENES"

	return dataframe


def main(fName, dirName):

	master_list = get_shared(fName, dirName)
	dataframe = compare_shared(master_list[0], master_list[1], master_list[2], master_list[3], master_list[4])
	if not dataframe.empty: 
		with open( dirName + fName[:-4] + "_diff_shared_FC.csv", 'wt' ) as writer:
			dataframe.to_csv(writer, index=False)

def runOnDir(dirName):
	# improve this by opening homeolog list here
	if (dirName[-1] != '/'):
		dirName += '/'
	filenames = next(os.walk(dirName))[2]

	for fName in filenames:
		if ('DESeq2') in fName:
			print "Running on file:",  fName
			main(fName, dirName)

if __name__ == "__main__":
	# arg parser implementation
	parser = argparse.ArgumentParser(description="Find differences in fold changes among homeologs")
	parser.add_argument("Directory")
	args = parser.parse_args()

	runOnDir(args.Directory)













