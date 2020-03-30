#!/usr/bin/env python
import csv, sys, numpy, math, pandas
from tqdm import tqdm
"""
Takes two gene list in csv format and outputs the unique genes between the lists in a new csv file
Include the rank of the gene in its parent list, log2FoldChange and padj 

USAGE: unique_finder.py <genelist1.csv> <genelist2.csv> <output_dir>
OUTPUT: genelist1_symmetirc_difference_results.csv genelist2_symmetirc_difference_results.csv 

Genes unique to the first list input are one rank less than expected 
Genes unique to the second list input are one rank lore than expected 

TODO: Order output gene list in order found

By Ronald Cutler
Updated 170824
"""

def unique_finder(file1reader, file2reader):
	
	
	list1 = []
	list1 = file1reader['Gene'] # put all the genes into a list, ordered by padj

	list2 = []
	list2 = file2reader['Gene']

	list3 = []
	list3 = list(set(list1).symmetric_difference(set(list2))) # compare the first item of both list, then the first & second of both, etc.
	
	if len(list3) <= 0:
		print ("NO UNIQUE GENES\n")
		return
	# search for the items in list3 against list 1 & 2 to find parent list index number and respective parent list.
	
	index_store = [] # storing the indexes of each symmetric differnce particular to its parent list 
	list_store = [] # storing the parent list of each symmetric difference
	# slicing out path names in DESeq file names 
	genelist1 = slice_name(filename1)
	genelist2 = slice_name(filename2)

	print ("\nStep 1: Getting rank of unique genes in parent lists\n")
	for item in tqdm(list3): # iterating through both list to search for origin of symmetric differnce
		count = 0 # reset count
		for list1_item in list1:
			if item == list1_item:
				index_store.append(count) # index of gene in respective list 
				list_store.append(genelist1)
				break
			else:
				count += 1
		# need to prevent this loop from working when we already found the gene in list1 
		count = 0 # reset count
		for list2_item in list2:
			if item == list2_item:
				index_store.append(count)
				list_store.append(genelist2)
				break
			else:
				count += 1

	# use index to find the associated rank of the gene in sym_dif 
	

	count = 0
	lfc_store = []
	padj_store = []

	columns = list(file1reader)
	lfc_index = columns.index('GFPvsDBM.dispersion.log2FC.0')
	padj_index = columns.index('FDR.dispersion')

	# iterating through list_store to get the lfc and padj 
	print ("\nStep 2: Getting log2 fold change & padj values of unique genes\n")
	for item in tqdm(list_store):
		gene_index = index_store[count] # getting the fold change at the index of the gene index at the position that corresponds with count

		if item == genelist1:
			lfc_store.append(file1reader.iloc[gene_index, lfc_index]) 
			padj_store.append(file1reader.iloc[gene_index, padj_index])
		else:
			lfc_store.append(file2reader.iloc[gene_index, lfc_index])
			padj_store.append(file2reader.iloc[gene_index, padj_index])

		count += 1 



	# splitting unique list into two separate list
	genelist1_genes = []
	genelist1_lfc = []
	genelist1_padj = []
	genelist1_rank = []

	genelist2_genes = []
	genelist2_lfc = []
	genelist2_padj = []
	genelist2_rank = []

	count = 0 
	for item in list_store:
		if item == genelist1:
			genelist1_genes.append(list3[count])
			genelist1_lfc.append(lfc_store[count])
			genelist1_padj.append(padj_store[count])
			genelist1_rank.append(index_store[count])
		else:
			genelist2_genes.append(list3[count])
			genelist2_lfc.append(lfc_store[count])
			genelist2_padj.append(padj_store[count])
			genelist2_rank.append(index_store[count])
		count +=1 


	#converting to numpy object
	genelist1_genes = numpy.array(genelist1_genes)
	genelist1_lfc = numpy.array(genelist1_lfc)
	genelist1_padj = numpy.array(genelist1_padj)
	genelist1_rank = numpy.array(genelist1_rank)

	genelist2_genes = numpy.array(genelist2_genes)
	genelist2_lfc = numpy.array(genelist2_lfc)
	genelist2_padj = numpy.array(genelist2_padj)
	genelist2_rank = numpy.array(genelist2_rank)
	
 
	# dictionary building pandas data frame
	dataframe1 = pandas.DataFrame({'unique_genes' : genelist1_genes, 'parent_rank' : genelist1_rank, 'log2FoldChange' : genelist1_lfc, 'padj' : genelist1_padj})
	# re-ordering columns to reflect above (default is to arrange alphabetical order)
	cols1 = dataframe1.columns.tolist()
	cols1 = ['unique_genes', 'parent_rank', 'log2FoldChange', 'padj']
	dataframe1 = dataframe1[cols1]

	# dictionary building pandas data frame
	dataframe2 = pandas.DataFrame({'unique_genes' : genelist2_genes, 'parent_rank' : genelist2_rank, 'log2FoldChange' : genelist2_lfc, 'padj' : genelist2_padj})
	# re-ordering columns to reflect above (default is to arrange alphabetical order)
	cols2 = dataframe2.columns.tolist()
	cols2 = ['unique_genes', 'parent_rank', 'log2FoldChange', 'padj']
	dataframe2 = dataframe2[cols2]

	dataframe_list = [dataframe1, dataframe2]

	return dataframe_list

#cuts out the path and and only returns the sample name
def slice_name(str):
	new_string = ''
	for i in reversed(str): #reading in str reversed
		if i != '/': #stopping building once we hit '/'
			new_string += i
		else:
			new_string = new_string[::-1] #re-reversing
			if new_string.endswith('.csv'):
				new_string = new_string[:-4]
			return new_string

if __name__ == "__main__":
	#setting global as used in unique_finder
	global filename1
	global filename2

	filename1 = sys.argv[1]
	filename2 = sys.argv[2]
	dirName1 = sys.argv[3] # output directory

	if dirName1[:-1] != '/':
		dirName1 = dirName1 + '/'

	with open(filename1) as file1:
		file1reader = pandas.read_csv(file1)

	with open(filename2) as file2:
		file2reader = pandas.read_csv(file2)

	dataframe_list = unique_finder(file1reader, file2reader)


	with open((dirName1 + slice_name(filename1) + "_symmetirc_difference_results.csv"), 'wt') as file3:
		dataframe_list[0].to_csv(file3, index=False) # do not write index column
	with open((dirName1 + slice_name(filename2) + "_symmetirc_difference_results.csv"), 'wt') as file4:
		dataframe_list[1].to_csv(file4, index=False) # do not write index column



