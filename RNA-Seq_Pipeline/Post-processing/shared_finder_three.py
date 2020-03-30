#!/usr/bin/env python
import csv, sys, numpy, math, pandas, os
from tqdm import tqdm
"""
Takes two gene list in csv format and outputs the sahred genes between the lists in a new csv file
Include the rank of the gene in its parent list, log2FoldChange and padj 

IMPORTANT: THIS IS MEANT TO BE RUN ON TRIMMED LIST OF SIGNIFICANT GENES RANKED BY PADJ VALUE 

USAGE: shared_finder_three.py <gene_list_dir_1> <gene_list_dir_2> <gene_list_dir_3> <output_dir>
OUTPUT: output_dir_genelist1.csv_shared_results.csv


TODO: Order output gene list in order found, add options for directories (roundRobin) or single files (change global vars)
	Rank pairs of shared genes by lowest average padj 
	Improve efficieny O(n^2) really slow?

By Ronald Cutler
Updated 181215 by JDN
"""

	
def shared_finder(file1reader, file2reader, file3reader):
	
	
	list1 = []
	list1 = file1reader[file1reader.columns[0]] # put all the genes into a list, ordered by padj

	list2 = []
	list2 = file2reader[file2reader.columns[0]]

	list3 = []
	list3 = file3reader[file3reader.columns[0]]

	list4 = []
	list4 = list(set(list1) & (set(list2)) & (set(list3))) # compare the first item of both list, then the first & second of both, etc.

	# if there is no intersection between gene lists
	if len(list4) <= 0:
		print("\nNO SHARED GENES\n")
		return

	print(len(list4))

	# search for the items in list3 against list 1 & 2 to find parent list index number and respective parent list.
	# this will give us two list of the same size. index_store will tell us which index to look for info and 
	# list_store will tell us which csv to look in
	
	index_store = [] # storing the indexes of each symmetric differnce particular to its parent list 
	list_store = [] # storing the parent list of each symmetric difference
	
	"""
	# For use with directories
	genelist1 = fName1
	genelist2 = fName2
	"""
	# For use with single files. slicing out path names in DESeq file names. These will be used to store in list_store.
	genelist1 = slice_name(fName1)
	genelist2 = slice_name(fName2)
	genelist3 = slice_name(fName3)
	

	# doubling occurence of each element in the shared list because those are in both of the parent list
	shared = []
	for i in list4:
		shared.extend([i, i, i])

	print("\nStep 1: Getting rank of shared genes in parent lists\n")
	for item in tqdm(list4): # iterating through both list to search for the rank of each shared element
		# searching list 1 for shared gene
		count = 0 # reset count
		for list1_item in list1:
			if item == list1_item:
				index_store.append(count) # index of gene in respective list 
				list_store.append(genelist1)
				break
			else:
				count += 1
		# searching list 2 for shared gene
		count = 0 # reset count
		for list2_item in list2:
			if item == list2_item:
				index_store.append(count)
				list_store.append(genelist2)
				break
			else:
				count += 1
		# searching list 3 for shared gene
		count = 0 # reset count
		for list3_item in list3:
			if item == list3_item:
				index_store.append(count)
				list_store.append(genelist3)
				break
			else:
				count += 1

	# use index to find the associated rank of the gene in shared
	
	count = 0
	lfc_store = []
	padj_store = []

	columns = list(file1reader)
	lfc_index = columns.index('log2FoldChange')
	padj_index = columns.index('padj')
	# for going through
	#lfc_index = columns[5]
	#padj_index = columns.index('FDR.dispersion')

	print("\nStep 2: Getting log2 fold change & padj values of shared genes\n")
	for item in tqdm(list_store): # iterating through list_store to get the lfc and padj
		gene_index = index_store[count] # getting the gene index stored in index_store for that shared gene in that list
		# from csv, writing lfc and padj to respective list
		# account for the new name column that was added
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

	# adding 1 to the ranks to account for headers
	index_store = [x + 1 for x in index_store]

	# converting to numpy objects
	lfc = numpy.array(lfc_store)
	padj = numpy.array(padj_store)
	parent_list = numpy.array(list_store)
	rank = numpy.array(index_store) 
	shared = numpy.array(shared) 

	"""
	For Debuging

	print "lfc len", len(lfc)
	print lfc, '\n'

	print "padj len", len(padj)
	print padj, '\n'

	print "parent list len", len(parent_list)
	print parent_list, '\n'

	print "rank len", len(rank)
	print rank, '\n'

	print "shared len", len(shared)
	print shared, '\n'
	"""

	# dictionary building pandas data frame
	dataframe = pandas.DataFrame({'shared_genes' : shared, 'parent_list' : parent_list, 'parent_rank' : rank, 'log2FoldChange' : lfc, 'padj' : padj})
	# re-ordering columns to reflect above (default is to arrange alphabetical order)
	cols = dataframe.columns.tolist()
	cols = ['shared_genes', 'parent_list', 'parent_rank', 'log2FoldChange', 'padj']
	dataframe = dataframe[cols]

	return dataframe

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
def roundRobin(dirName1, dirName2, dirName3, dirName4):
	#setting global as used in shared_finder
	global fName1
	global fName2
	global fName3

	filenames1 = next(os.walk(dirName1))[2]
	filenames2 = next(os.walk(dirName2))[2]
	filenames3 = next(os.walk(dirName3))[2]

	for fName1 in filenames1:
		if 'DESeq2' in fName1:
			with open(dirName1 + fName1) as file1:
					file1reader = pandas.read_csv(file1)
			for fName2 in filenames2:
				if 'DESeq2' in fName2:
					with open(dirName2 + fName2) as file2:
						file2reader = pandas.read_csv(file2)
					for fName3 in filenames3:
						if 'DESeq2' in fName3:
							print('\nRunning with ' + fName1 + ' and ' + fName2 + ' and ' + fName3 + '\n')

							with open(dirName3 + fName3) as file3:
								file3reader = pandas.read_csv(file3)

							data = shared_finder(file1reader, file2reader, file3reader)

						if data is not None:
						# trimming file 1 name
							if fName1.endswith('.csv'):
									fName1 = fName1[:-4]

							with open((dirName3 + fName1 + "_" + fName2 + "_shared_results.csv"), 'wt') as file3:
								data.to_csv(file3, index=False) # do not write index column	
						else:
							continue
if __name__ == "__main__":
	"""
	# Directory roundRobin
	dirName1 = sys.argv[1]
	dirName2 = sys.argv[2]
	dirName3 = sys.argv[3]

	if dirName1[:-1] != '/':
		dirName1 = dirName1 + '/'
	if dirName2[:-1] != '/':
		dirName2 = dirName2 + '/'
	if dirName3[:-1] != '/':
		dirName3 = dirName3 + '/'
		
	roundRobin(dirName1, dirName2, dirName3)
	"""
	# Single Files 
	global fName1
	global fName2
	global fName3

	fName1= sys.argv[1]
	fName2 = sys.argv[2]
	fName3 = sys.argv[3]
	dirName1 = sys.argv[4] # output directory

	if dirName1[:-1] != '/':
		dirName1 = dirName1 + '/'

	with open(fName1) as file1:
		file1reader = pandas.read_csv(file1)

	with open(fName2) as file2:
		file2reader = pandas.read_csv(file2)

	with open(fName3) as file3:
		file3reader = pandas.read_csv(file3)

	data = shared_finder(file1reader, file2reader, file3reader)

	if data is not None:
		# trimming filename1
		if fName1.endswith('.csv'):
			fName1 = fName1[:-4]

		with open((dirName1 + slice_name(fName1) + "_" + slice_name(fName2) + "_" + slice_name(fName3) + "_shared_results.csv"), 'wt') as file4:
			data.to_csv(file4, index=False) # do not write index column
	else:
		exit()