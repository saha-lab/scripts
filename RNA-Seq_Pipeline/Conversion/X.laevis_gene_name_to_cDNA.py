#!/usr/bin/env python
"""
Changes the gene names in a count file if they are unnamed to the 
names that are associated with the same JGI Gene ID in the cDNA fasta 
file that corresponds to the same annotation

USAGE: gene_name_to_cDNA.py <in_counts_dir> <out_counts_dir> <cDNA_fasta>

Output: new directory of modified gene names and counts

Updated 170923 by Ronald Cutler
"""
import csv, sys, os
from tqdm import tqdm

def main(filename1, dirName, outDir, cDNA ):
	cDNA_names = []
	cDNA_IDs = []

	with open( cDNA, 'r') as reader1:
		for line in reader1:
			if '>' in line:
				cDNA_names.append(line[1:].rstrip('\n'))
				cDNA_IDs.append(line.split('|')[1].rstrip('\n'))

	
	with open(dirName + filename1, 'r') as file1:	
		with open(outDir + filename1, 'w') as file2:
			print "\nRenaming Genes\n"
			count = 0
			for line in tqdm(file1):
				if ("unnamed" in line) or ("loc") in line:
					if line.count('|') == 2:
						ID1 = line.split('\t')[0].split('|')[1] # gets the first ID
						ID2 = line.split('\t')[0].split('|')[2] # gets the second ID
						gene_count = line.split('\t')[1]
						if (ID1 in cDNA_IDs) and (ID2 in cDNA_IDs):
							line = cDNA_names[cDNA_IDs.index(ID1)]
							file2.write(line + '|' + ID2 + '\t' + gene_count)
							count += 1
						else:
							file2.write(line)
					else:
						ID = line.split('\t')[0].split('|')[1] # get ID form count line. i.e. "unnamed|Xelaev18000001m	0"
						gene_count = line.split('\t')[1]
						if ID in cDNA_IDs:
							line = cDNA_names[cDNA_IDs.index(ID)]
							file2.write(line + '\t' + gene_count)
							count += 1
						else:
							file2.write(line)
				else:
					file2.write(line)

	print "Changed", count, "entries"

def runOnDirectory(dirName, outDir, cDNA):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		if ('.txt') in fName:
			print 'Running on file: ' + fName
			main(fName, dirName, outDir, cDNA)

if __name__ == "__main__":

	dirName = sys.argv[1]
	if (dirName[-1] != '/'):
		dirName += '/'
	outDir = sys.argv[2]
	if (outDir[-1] != '/'):
		outDir += '/'

	runOnDirectory(dirName, outDir, sys.argv[3])