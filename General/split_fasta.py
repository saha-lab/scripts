#!/usr/bin/env python
"""
Splits a fasta that has been interleaved into two separate paired-end read files
Outputs paired-end fasta pair of files in same directory
USAGE: split_fasta.py <interleaved.fasta>

Updated 170630 by Ronald Cutler
"""
import sys
from itertools import izip

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

def main( argv ):
	with open( argv, 'r' ) as reader:
		with open( argv + "_right.fasta", 'w') as writer1:
			with open( argv + "_left.fasta", 'w') as writer2:
				switch = False
				for x, y in pairwise(reader):
					if switch == False:
						writer1.write(x)
						writer1.write(y)
						switch = True
					else:
						writer2.write(x)
						writer2.write(y)
						switch = False

if __name__ == "__main__":
	main( sys.argv[1] )
