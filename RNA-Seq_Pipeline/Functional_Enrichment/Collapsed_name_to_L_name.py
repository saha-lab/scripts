#!usr/bin/env/python2

"""
Takes the DESeq2 output where homeologs have been collapsed and outputs a new csv with the homeolog
collapsed genes names converted into the L homeolog gene name. This is used for running for a GO
enrichment using BLAST2GO as homeolog collapsed genes names are not in the annotation and need to 
instead be searched and thus annotated as the L homeolog. This can introduce bias into the GO 
enrichment if the L and S homeolog are not similarly annotated. 

USAGE: Collapsed_name_to_L_name.py <collapsed_output.csv> 
"""

import pandas, sys, os
from tqdm import tqdm
def main(dirName, collapsed):

	# convert collapsed
	# list stay in same order
	new_list = []
	with open(dirName + collapsed) as filereader:
		filereader1 = pandas.read_csv(filereader)
		list1 = list(filereader1[filereader1.columns[0]])
		# split collapsed Gene IDs into respective lists
		for item in tqdm(list1):
			item_split = item.split('|')
			# collapsed name will split into 3
			if len(item_split) == 3:
				# add .L to the gene symbol and combine with gene ID
				# exceptions if already has .L or .S due to error in collapsing
				if item_split[0].endswith(".L"):
					L_name = item_split[0] + "|" + item_split[1]
				elif item_split[0].endswith(".S"):
					L_name = item_split[0][:-2] + ".L|" + item_split[1]
				else:
					L_name = item_split[0] + ".L|" + item_split[1]
				new_list.append(L_name)
			else:
				new_list.append(item)

	# create output csv
	shared = [('Gene', new_list)]
	df = pandas.DataFrame.from_items(shared)
	# Account for unique list headers 'unique_genes'
	if list(filereader1)[0] == 'unique_genes':
		filereader1['unique_genes'] = df['Gene']
	else:
		filereader1['Gene'] = df['Gene']

	with open(dirName + collapsed[:-4] + "_collapsed_name_change.csv", 'w') as filewriter:
		filereader1.to_csv(filewriter, index=False)

def runOnDir (dirName):
	filenames = next(os.walk(dirName))[2]
	dirName = dirName + "/"
	for fName in filenames:
		if ("DESeq2") in fName:
			print "Running on file: " + fName
			main(dirName, fName)

if __name__ == "__main__":
	runOnDir(sys.argv[1])
