#!/usr/bin/env python
"""
Takes a single FASTQ file and splits to .fasta + .qual files

USAGE: fastq_to_fasta.py <fastqIn.fastq>

Updated 180721 by Ronald Cutler
"""
import sys
from Bio import SeqIO

if len(sys.argv) == 1: 
	print "Please specify a  single .fastq file to convert."
	sys.exit()

filetoload = sys.argv[1]
basename = filetoload

#Chop the extension to get names for output files
if basename.find(".") != -1:
	basename = '.'.join(basename.split(".")[:-1])

SeqIO.convert(filetoload, "fastq", basename + ".fasta", "fasta")
SeqIO.convert(filetoload, "fastq", basename + ".qual", "qual")