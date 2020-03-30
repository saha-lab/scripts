#!/usr/bin/env python

"""
In a directory of Salmon quant.sf files, create
new csv files that contain only the gene name and TPM

USAGE: TPM_salmon.py <input_directory>

Updated 180506 by Ronald Cutler
"""

import csv, sys, os

def main( argv ):
	fastqfiles = [x[0] for x in os.walk(argv)]
	fastqfiles.pop(0)

	for folder in fastqfiles:
		filenames = [os.path.join(root, name)
	             for root, dirs, files in os.walk(folder)
	             for name in files
	             if "quant.sf" in name]

	 print("Running on:")
	   	for file in filenames:
	   		print file
	   		f = open(file, 'r')
			csv_f = csv.reader(f, delimiter='\t')
			with open(file+"_tpms.txt", 'w') as writer:
				for row in csv_f:
					writer.write(row[0]+"\t"+row[3]+"\n") # to get the first and fourth columns

			f.close()

	

if __name__ == "__main__":
	main(sys.argv[1])
