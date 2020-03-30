#!/usr/bin/env python
"""
Converts a genbank annotation + sequence file to a fasta file

USAGE: gb_to_fasta.py <input.gb> <output.fasta>

Last updated 180721 by Ronald Cutler
"""

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys

gb_filename   = sys.argv[1]
if not gb_filename.endswith(".gb"):
	print("Error: Invalid filename " + gb_filename + ". Are you sure it's a GFF?")
#end if

with open(gb_filename, 'rU') as gb_file_handle:
	# First and only record is the sequence, which contains a list of all features.	
	gb_root = SeqIO.read(gb_file_handle, "genbank")
	sequence = gb_root.seq

	sequence_list = []
	for cds in filter(lambda x: x.type == "CDS", gb_root.features):
		cds_sequence = cds.extract(sequence).translate()
		cds_record = SeqRecord(cds_sequence)

		cds_record.id = reduce(lambda x,y: x + "|" + y, cds.qualifiers["locus_tag"])
		if "gene" in cds.qualifiers:
			cds_record.id += " (" + reduce(lambda x, y: x + "|" + y, cds.qualifiers["gene"]) + ")"
		#end if
		cds_record.description = reduce(lambda x, y: x + "|" + y, cds.qualifiers["product"])

		sequence_list.append(cds_record)
	#for cds
#end with 

fasta_filename = sys.argv[2]
with open(fasta_filename, 'w') as fast_file_handle:
	SeqIO.write(sequence_list, fast_file_handle, 'fasta')
#end with