#!/usr/bin/env python
"""
Changes the gene names in DESeq2 csv output if they are unnamed to the 
names that are associated with the same JGI Gene ID in the cDNA fasta 
file that corresponds to the same annotation (taejoon V4)

This is exclusively for Xenopus laevis. The cDNA file currently used is at: 
/Volumes/cachannel-1/DNA-SEQ/Xenopus/Reference_Sequences/laevis/v9.1/XENLA_JGIv18pV4_cdna.fa

USAGE: X.laevis_unaamed_conversion.py <DESeq2_output_dir> <cDNA_fasta>

Updated 170627 by Ronald Cutler
"""
import csv, sys, os
from tqdm import tqdm

def add_gene_header(filename1, dirName, cDNA ):
	cDNA_names = []
	cDNA_IDs = []

	# open file for editing
	with open(dirName + filename1, 'r') as file1:
		data = [row for row in csv.reader(file1)] # getting a 2d list representation of the csv 

	with open( cDNA, 'r') as reader1:
		for line in reader1:
			if '>' in line:
				cDNA_names.append(line[1:].rstrip('\n'))
				cDNA_IDs.append(line.split('|')[1].rstrip('\n'))

	#edit the first cell (0,0)
	with open(dirName + filename1, 'w') as file2:
		writer = csv.writer(file2)
		data[0][0] = 'gene'
		
		print "\nRenaming Genes\n"
		for row in tqdm(data):
			if 'gene' in row[0]:
				writer.writerow(row)
			elif ('unnamed' in row[0]) or ('LOC' in row[0]):
				ID = row[0].split('|')[1]
				if ID in cDNA_IDs:
					row[0] = cDNA_names[cDNA_IDs.index(ID)]
					writer.writerow(row)
			else:
				writer.writerow(row)

"""
Runs add_gene_header on all DE list in directory 
"""
def runOnDirectory(dirName, cDNA):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		if ('DESeq2') in fName:
			print '\nRunning on file: ' + fName
			add_gene_header( fName, dirName, cDNA )

if __name__ == "__main__":

	dirName = sys.argv[1]
	cDNA = sys.argv[2]
	if (dirName[-1] != '/'):
		dirName += '/'
	runOnDirectory(dirName, cDNA)