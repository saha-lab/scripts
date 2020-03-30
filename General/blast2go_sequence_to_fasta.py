#!usr/bin/env python2

"""
Generates fasta output from BLAST2GO

USAGE: blast2go_sequence_to_fasta.py <blast2go_sequence_output.fasta>

Updated by Ronald CUter 180108
"""

import sys

def main(inFile):

	# open file and write to new file
	with open(inFile, 'r') as reader:
		with open(inFile[:-6] + "_new.fasta", 'w') as writer:
			for line in reader:
				if "Sequence" in line:
					continue
				split = line.split(',')
				writer.write(">" + split[0] + '\n' + split[1])



if __name__ == "__main__":
	main(sys.argv[1])