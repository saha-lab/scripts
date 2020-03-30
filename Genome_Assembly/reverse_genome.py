#!/usr/bin/env python

"""
Reverses the base ordering of a genome, but does not complement!

USAGE: reverse_genome.py <genome_in.fasta> <reverse_genome_out.fasta>

Updated 180721 by Ronald Cutler
"""
import sys

file_in = sys.argv[1]
file_out = sys.argv[2]

with open(file_out, "w") as out:
	for line in reversed(open(file_in).readlines()):
		out.write(line.rstrip())

