#!/usr/bin/env python
"""
Given a directory of csv files with gene names in the first column, add a second column with
the coresponding gene descriptions given in a mapping file and replace the old csv
The current mappng file used for uncollapsed X. laevis gene names is 
loacted at: /Volumes/cachannel/RNA_SEQ/Analysis/Reference/X_laevis/9.1_Reference_Files/Functional_annotation/XenopusLaevis_GeneID_Description.txt

Input: <gene_description_mapping_file> <dir_name> [output folder]
Note the output folder argument is optional

Updated 180506 by Ronald Cutler
"""
import csv, pandas, sys, os

def main(gene, gene_csvIn, dirName, outName):

	# iterate through the first column of the csv and find gene 
	with open(dirName + "/" + gene_csvIn) as file1:
		filereader1 = pandas.read_csv(file1) 

	geneList = list(filereader1[filereader1.columns[0]])
	data = []
	for item in geneList:
		if item == gene:
			print("Gene found in ", gene_csvIn)
			# add to new output
			print("index", geneList.index(item))
			print(filereader1.iloc[geneList.index(item)])
			data.append(dict(filereader1.iloc[geneList.index(item)]))

	df = pandas.DataFrame(data)
	print(df)
	# add the column to the data frame 
	cols = filereader1.columns.tolist()

	# write new dataframe 
	with open(outName + gene_csvIn[:-3]+ "_found_genes.csv", 'wt') as fileOut:
		df.to_csv(fileOut, index = False)

def runOnDir(gene, dirName, outName):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		if fName.endswith('.csv'):
			print("Running on file:",  fName)
			main(gene, fName, dirName, outName)

if __name__ == "__main__":
	outName = sys.argv[3]
	if (outName[-1] != '/'):
		outName += '/'
	runOnDir(sys.argv[1], sys.argv[2], outName)
		
	