#!/usr/bin/env python
"""
Takes an SDE list and a list of genes to filter. 
Outputs a new SDE list with genes filtered out.
Updated 170824 by Ronald Cutler
"""
import sys, pandas, numpy
def shared_finder(file1reader, file2reader):
	
	
	list1 = []
	list1 = file1reader['gene'] # put all the genes into a list, ordered by padj

	list2 = []
	list2 = file2reader['gene']

	list3 = []
	list3 = list(set(list1) & (set(list2))) # compare the first item of both list, then the first & second of both, etc.

	# if there is no intersection between gene lists
	if len(list3) <= 0:
		print "\nNO SHARED GENES\n"
		return

	index_store = []
	gene_list = []

	count = 0
	for item in list1:
		if item not in list3:
			index_store.append(count)
			gene_list.append(item)
		count +=1

	lfc_store = []
	padj_store = []

	for index in index_store:
		lfc_store.append(file1reader.iloc[index, 2]) 
		padj_store.append(file1reader.iloc[index, 6])

	index_store = [x + 1 for x in index_store]

	lfc = numpy.array(lfc_store)
	padj = numpy.array(padj_store)
	rank = numpy.array(index_store) 

	dataframe = pandas.DataFrame({'gene' : gene_list, 'pre-filter_rank' : rank, 'log2FoldChange' : lfc, 'padj' : padj})
	cols = dataframe.columns.tolist()
	cols = ['gene', 'pre-filter_rank', 'log2FoldChange', 'padj']
	dataframe = dataframe[cols]

	print "\nFiltered List length:", len(gene_list), "\n"
	return dataframe

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
	global fName1
	global fName2

	fName1= sys.argv[1]
	fName2 = sys.argv[2]
	dirName1 = sys.argv[3] # output directory

	if dirName1[:-1] != '/':
		dirName1 = dirName1 + '/'

	with open(fName1) as file1:
		file1reader = pandas.read_csv(file1)

	with open(fName2) as file2:
		file2reader = pandas.read_csv(file2)

	data = shared_finder(file1reader, file2reader)

	if data is not None:
		# trimming filename1
		if fName1.endswith('.csv'):
			fName1 = fName1[:-4]

		with open((dirName1 + slice_name(fName1) + "_" + slice_name(fName2) + "_filtered_results.csv"), 'wt') as file3:
			data.to_csv(file3, index=False) # do not write index column
	else:
		exit()