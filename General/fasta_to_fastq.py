#!/usr/bin/env python
import sys
from Bio import SeqIO
from Bio.SeqIO.QualityIO import PairedFastaQualIterator

"""
Takes a FASTA file, which must have a corresponding .qual quality 
file with the same basename, e.g sample.fasta & sample.qual, 
and creates a single FASTQ file.

USAGE: fasta_to_fastq.py <sequenceIn.fasta>

Updated 180721 by Ronald Cutler
"""

if len(sys.argv) == 1:
        print "Please specify a single FASTA file to convert."
        sys.exit()

filetoload = sys.argv[1]
basename = filetoload

#Chop the extension to get names for output files
if basename.find(".") != -1:
        basename = '.'.join(basename.split(".")[:-1])

try:
	fastafile = open(filetoload)
	qualfile = open(basename + ".qual")
except IOError:
	print "Either the file cannot be opened or there is no corresponding"
	print "quality file (" + basename +".qual)"
	sys.exit()

rec_iter = PairedFastaQualIterator(fastafile,qualfile)

SeqIO.write(rec_iter, open(basename + ".fastq", "w"), "fastq")