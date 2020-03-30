#!/usr/bin/env python
import sys
"""
Copying "Name" field in gff3 file in the gene entry line 
and adding on the "ID" field to the name field and copying 
to all CDS entry lines for that gene

e.g. 
Old: ID=Xeale0394m.g;Name=egfl6.S
New: ID=Xeale0394;Name=egfl6.S|Xeale0394
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
				ID = name[0][3:]
				if ID[-2:] == ".g":
					ID = ID[:-2]
				name = name[1]
				writer.write(line.rstrip('\n') + '|' + ID + '\n')

			elif split_line[2] == "CDS":
				new_name = split_line[8].rstrip('\n') + ";" + name.rstrip('\n') + '|' + ID + '\n'
				split_line[8] = new_name
				writer.write('\t'.join(split_line))

			else:
				writer.write(line)

		writer.close( )
	

if __name__ == "__main__":
	main( sys.argv ) 