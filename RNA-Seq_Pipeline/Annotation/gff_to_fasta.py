from BCBio import GFF
from Bio import SeqIO
import sys

gff_filename   = sys.argv[1]
if not gff_filename.endswith(".gff"):
	print("Error: Invalid filename " + gff_filename + ". Are you sure it's a GFF?")
#end if

fasta_filename = sys.argv[2]

sequence = SeqIO.read(fasta_filename, "fasta")

with open(gff_filename, 'rU') as gff_file_handle:
	# First and only record is the sequence, which contains a list of all features.
	gff_root = GFF.parse(gff_file_handle).next()
	for cds in filter(lambda x: x.type == "CDS", gff_root.features):
		cds_sequence = cds.extract(sequence)

		cds_sequence.id = reduce(lambda x,y: x + "|" + y, cds.qualifiers["locus_tag"])
		if "gene" in cds.qualifiers:
			cds_sequence.id += " (" + reduce(lambda x, y: x + "|" + y, cds.qualifiers["gene"]) + ")"
		#end if
		cds_sequence.description = reduce(lambda x, y: x + "|" + y, cds.qualifiers["product"])

		print(cds_sequence.format("fasta"))
	#for cds
#end with 