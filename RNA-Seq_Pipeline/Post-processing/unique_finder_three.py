#!/usr/bin/env python
import csv, sys, numpy, math, pandas
from tqdm import tqdm
"""
Takes two gene list in csv format and outputs the unique genes between the lists in a new csv file
Include the rank of the gene in its parent list, log2FoldChange and padj 

USAGE: unique_finder.py <genelist1.csv> <genelist2.csv> <genelist2.csv> <output_dir>
OUTPUT: genelist1_symmetirc_difference_results.csv genelist2_symmetirc_difference_results.csv genelist3_symmetirc_difference_results.csv

Genes unique to the first list input are one rank less than expected 
Genes unique to the second list input are one rank more than expected 

TODO: Order output gene list in order found

By Ronald Cutler & LeAnn Lo
Updated 180506
"""

def unique_finder(file1reader, file2reader, file3reader):
	
	
	list1 = []
	list1 = file1reader['gene'] # put all the genes into a list, ordered by padj

	list2 = []
	list2 = file2reader['gene']

	list3 = []
	list3 = file3reader['gene']

	list4 = []
	list4 = list(set(list1).symmetric_difference(set(list2))) # compare the first item of both list, then the first & second of both, etc.

	list5 = []
	list5 = list(set(list3).symmetric_difference(set(list4)))

	#take the shared between all three, then take the symmetric difference of 5 and 6

	list6 = []
	list6 = list(set(list1) & (set(list2)) & (set(list3))) 

	list7 = []
	list7 = list(set(list5).symmetric_difference(set(list6)))

	if len(list7) <= 0:
		print ("NO UNIQUE GENES\n")
		return

	# convert pandas objects to lists
	list1 = list(list1)
	list2 = list(list2)
	list3 = list(list3)
	
	index_store = [] # storing the indexes of each symmetric differnce particular to its parent list 
	list_store = [] # storing the parent list of each symmetric difference

	# slicing out path names in DESeq file names 
	genelist1 = slice_name(filename1)
	genelist2 = slice_name(filename2)
	genelist3 = slice_name(filename3)
	
	print ("\nStep 1: Getting rank of unique genes in parent lists\n")
	for item in tqdm(list7): # iterating through both list to search for origin of symmetric differnce
		if item in list1:
			index_store.append(list1.index(item))
			list_store.append(genelist1)
		elif item in list2:
			index_store.append(list2.index(item))
			list_store.append(genelist2)
		elif item in list3:
			index_store.append(list3.index(item))
			list_store.append(genelist3)
	
	# use index to find the associated rank of the gene in sym_dif 
	lfc_store = []
	padj_store = []

	columns = list(file1reader)
	lfc_index = columns.index('log2FoldChange')
	padj_index = columns.index('padj')

	# iterating through list_store to get the lfc and padj 
	print ("\nStep 2: Getting log2 fold change & padj values of unique genes\n")
	count = 0
	for item in tqdm(list_store):
		gene_index = index_store[count] # getting the fold change at the index of the gene index at the position that corresponds with count

		if item == genelist1:
			lfc_store.append(file1reader.iloc[gene_index, lfc_index]) 
			padj_store.append(file1reader.iloc[gene_index, padj_index])
		if item == genelist2:
			lfc_store.append(file2reader.iloc[gene_index, lfc_index])
			padj_store.append(file2reader.iloc[gene_index, padj_index])
		if item == genelist3:
			lfc_store.append(file3reader.iloc[gene_index, lfc_index])
			padj_store.append(file3reader.iloc[gene_index, padj_index])

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

	genelist3_genes = []
	genelist3_lfc = []
	genelist3_padj = []
	genelist3_rank = []

	# rank is off by 1, adding 1 to account for this. This does not effect the indexing
	count = 0 
	for item in list_store:
		if item == genelist1:
			genelist1_genes.append(list7[count])
			genelist1_lfc.append(lfc_store[count])
			genelist1_padj.append(padj_store[count])
			genelist1_rank.append(index_store[count] + 1)
		if item == genelist2:
			genelist2_genes.append(list7[count])
			genelist2_lfc.append(lfc_store[count])
			genelist2_padj.append(padj_store[count])
			genelist2_rank.append(index_store[count] + 1)
		if item == genelist3:
			genelist3_genes.append(list7[count])
			genelist3_lfc.append(lfc_store[count])
			genelist3_padj.append(padj_store[count])
			genelist3_rank.append(index_store[count] + 1)
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
	
	genelist3_genes = numpy.array(genelist3_genes)
	genelist3_lfc = numpy.array(genelist3_lfc)
	genelist3_padj = numpy.array(genelist3_padj)
	genelist3_rank = numpy.array(genelist3_rank)
 
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

	# dictionary building pandas data frame
	dataframe3 = pandas.DataFrame({'unique_genes' : genelist3_genes, 'parent_rank' : genelist3_rank, 'log2FoldChange' : genelist3_lfc, 'padj' : genelist3_padj})
	# re-ordering columns to reflect above (default is to arrange alphabetical order)
	cols3 = dataframe3.columns.tolist()
	cols3 = ['unique_genes', 'parent_rank', 'log2FoldChange', 'padj']
	dataframe3 = dataframe3[cols3]

	dataframe_list = [dataframe1, dataframe2, dataframe3]

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
	global filename3

	filename1 = sys.argv[1]
	filename2 = sys.argv[2]
	filename3 = sys.argv[3]
	dirName1 = sys.argv[4] # output directory

	if dirName1[:-1] != '/':
		dirName1 = dirName1 + '/'

	with open(filename1) as file1:
		file1reader = pandas.read_csv(file1)

	with open(filename2) as file2:
		file2reader = pandas.read_csv(file2)

	with open(filename3) as file3:
		file3reader = pandas.read_csv(file3)

	dataframe_list = unique_finder(file1reader, file2reader, file3reader)

	with open((dirName1 + slice_name(filename1) + "_symmetric_difference_results.csv"), 'wt') as file3:
		dataframe_list[0].to_csv(file3, index=False) # do not write index column
	with open((dirName1 + slice_name(filename2) + "_symmetric_difference_results.csv"), 'wt') as file4:
		dataframe_list[1].to_csv(file4, index=False) # do not write index column
	with open((dirName1 + slice_name(filename3) + "_symmetric_difference_results.csv"), 'wt') as file5:
		dataframe_list[2].to_csv(file5, index=False) # do not write index column



