#!/usr/bin/env python
"""
Takes in a SDE list of genes output from DESeq-2 and 
searches their names in a uniprot fasta proteome database. 
Outputs a list of searchable gene names that were found in database. 

Known Bugs: Will output duplicate names for some genes 

"""


import sys, os, re
from tqdm import tqdm

def main( dirName, fName, database ):
	# strip names in DE list 
	with open(dirName+fName, 'rU') as f:
		fLines = f.readlines()

	lines = []
	for line in fLines:
			# modified for input with just gene names already timmed
			#line = line.split( '|' )
			#line = line[0]

			lines.append(line.upper( ).rstrip("\n"))
	
	# search database 
	count = 0
	start_len = len(lines)

	with open(database, 'rU') as data_read:
		writer = open(dirName + fName + '_uniprot_found.txt', 'w')

		for line in data_read:
			if '>' in line:
				split_line = line.split(" ")
				#print split_line
				for gene in lines:
					if gene == split_line[0].split("|")[2].split("_")[0]: # looking for this kind of entry: >sp|O93400|ACTB_XENLA Actin, cytoplasmic 1 OS=Xenopus laevis GN=actb PE=2 SV=1
						print "PRIMARY FOUND", gene
						writer.write( split_line[0].split("|")[2] + "\n")
						lines.remove( gene )
						count += 1
						break
					else: # looking for this kinf of entry: >tr|Q7ZZZ3|Q7ZZZ3_XENLA Putative growth hormone like protein-1 OS=Xenopus laevis GN=higd1a PE=2 SV=1
						for entry in split_line:
							if "GN=" + gene.lower( ) == entry:
								print "SECONDARY FOUND", gene
								writer.write( split_line[0].split("|")[2] + "\n" )
								lines.remove( gene )
								count += 1
								break
							elif "GN=" + gene.upper( ) == entry:
								print "SECONDARY FOUND", gene
								writer.write( split_line[0].split("|")[2] + "\n" )
								lines.remove( gene )
								count += 1
								break
		
		writer.close( )

	# writing genes not found
	with open(dirName + fName + "_not_found.txt", 'w') as writer_1:
		for line in lines:
			writer_1.write(line + "\n")

	print "Found: ", count, "/", start_len, " genes"

def runOnDirectory( dirName, database ):
	fileNames = next(os.walk(dirName))[2]
	for fName in tqdm(fileNames):
		if 'SDE' in fName:
			print 'Running on file: ' + fName
			main(dirName, fName, database)

if __name__ == "__main__":

	dirName = sys.argv[1]
	if(dirName[-1] != '/'):
		dirName += '/'
	database = sys.argv[2]

	runOnDirectory(dirName, database)
