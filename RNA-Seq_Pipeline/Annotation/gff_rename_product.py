/env python

import sys
"""
Copying "product" field in gff3 file in the 'CDS' entry line and copying to respective 'gene' entry line

Updated 180706 by Ronald Cutler
"""
def main( argv ):

	with open( sys.argv[1], 'r' ) as reader:
		writer = open (sys.argv[1] + "_out.gff", 'w' )
		name = ''
		product_names = []
		lines = []
		
		for line in reader:
			if "#" in line:
				writer.write(line)
				continue
			split_line = line.split('\t')

			features = ["CDS", "tRNA", "tmRNA", "rRNA", "ncRNA"]

			if split_line[2] in features:
				name = split_line[8].split(';')
				name = name[len(name)-1]
				writer.write(line)

			elif split_line[2] == "gene":
				new_name = split_line[8].rstrip('\n') + ";" + name
				split_line[8] = new_name
				writer.write('\t'.join(split_line))

			else:
				writer.write(line)

		writer.close( )
	

if __name__ == "__main__":
	main(sys.argv) 