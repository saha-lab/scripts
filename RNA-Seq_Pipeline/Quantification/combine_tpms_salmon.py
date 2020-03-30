#!/usr/bin/env python

"""
Combines the TPM counts in a salmon output directory that has TPMs already extracted from the quant.sf file into one csv file
USAGE: TPM_salmon.py input_directory
"""

import csv, sys, os, pandas

def main( argv ):
	fastqfiles = [x[0] for x in os.walk(argv)]
	fastqfiles.pop(0)

	frame = pandas.DataFrame()
	TPMs = []
	for folder in fastqfiles:
		print "Folder:", folder
		filenames = [os.path.join(root, name)
	             for root, dirs, files in os.walk(folder)
	             for name in files
	             if "quant.sf_tpms.txt" in name]

		print "Files: "
		for file in filenames:
			if len(filenames) > 0:
				print "Extracting from", file
				col_name = file.split('/')[-2]
				reader = pandas.read_csv(file, header = 0)
				reader = reader.rename({"TPM" : col_name})
				TPMs.append(reader)
		frame = pandas.concat(TPMs)
		frame.to_csv(path_or_buf=(argv +"_Combined_TPMs.csv"))
		"""
	   	for file in filenames:
	   		print file
	   		f = open(file, 'r')
			csv_f = csv.reader(f, delimiter='\t')
			with open(file+"_tpms.txt", 'w') as writer:
				for row in csv_f:
					writer.write(row[0]+"\t"+row[3]+"\n") # to get the first and fourth columns

			f.close()
		"""
	

if __name__ == "__main__":
	main(sys.argv[1])
