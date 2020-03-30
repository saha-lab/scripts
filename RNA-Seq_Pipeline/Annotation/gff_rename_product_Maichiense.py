#!/usr/bin/env python

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
			if "HerbertWM" in line:
				lines.append(line)
				continue
			if "Bernie" in line:
				lines.append(line)
				continue
			if "#" in line:
				lines.append(line)
				continue
			split_line = line.split('\t')

			features = ["CDS", "tRNA", "tmRNA", "rRNA", "ncRNA"]

			if split_line[2] in features:
				name = split_line[8].split(';')
				name = name[len(name)-3]
				product_names.append(name)
				lines.append(line)

			elif split_line[2] == "gene":
				lines.append(line)

			else:
				lines.append(line)

		counter = 0
		for line in lines:
			if "HerbertWM" in line:
				writer.write(line)
				continue
			elif "Bernie" in line:
				writer.write(line)
				continue
			elif "#" in line:
				writer.write(line)
				continue
			split_line = line.split('\t')

			if split_line[2] == "gene":
				new_name = split_line[8].rstrip('\n') + ";" + product_names[counter] + "\n"
				split_line[8] = new_name
				writer.write('\t'.join(split_line))
				counter += 1

			else:
				writer.write(line)

		writer.close( )
	

if __name__ == "__main__":
	main(sys.argv) 