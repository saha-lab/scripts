#!/usr/bin/env python

import sys
"""
Copying "Name" field in gff3 file in the gene entry line and copying to all CDS entry lines for that gene

Updated 170519 by Ronald Cutler
"""
def main( argv ):

	with open( sys.argv[1], 'r' ) as reader:
		writer = open (sys.argv[1] + "_out.gff", 'w' )
		name = ''
		for line in reader:
			if "#" in line:
				writer.write(line)
				continue
			split_line = line.split('\t')

			if split_line[2] == "gene":
				name = split_line[8].split(';')
				temp = name[0].replace("ID=gene-","Name=")
				name[1] = temp
				semicolon = ";"
				new_line = semicolon.join(name)
				writer.write(line)

			else:
				writer.write(line)

		writer.close( )
	

if __name__ == "__main__":
	main( sys.argv ) 