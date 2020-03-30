#!/usr/bin/env python
"""
For reading in a txt file of gene names on each line and a multi-fasta
database which contains the sequence associated with these name and 
returns a multi-fasta file of fasta entries corresponding to the input. 

USAGE: Extract_cDNA.py <geneList.txt> <multi_fasta.fasta> <output.txt>

Last updated 170811 by Ronald Cutler

TODO: Use fuzzy matching when names are not 1-1 match.
"""

import sys

def main(query, ref, output):

	geneList = []
	with open( query, 'r') as reader1:
		for line in reader1:
			geneList.append(line)

	hitList = []
	with open(ref, 'r') as reader2:
		for line in (reader2):
			if ">" in line:
				if line[1:] in geneList:
					hit = line + next(reader2) + '\n'
					hitList.append(hit)

	with open(output, 'w') as writer:
		for item in hitList:
			writer.write(item)



if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])