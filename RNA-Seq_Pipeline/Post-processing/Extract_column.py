#!/usr/bin/env python
"""
Gets all of the content that is in the first column of a csv
Skips the header to make content more iterable

Usage: Extract_header_column.py <Directory of files>
Output: Text files of the gene names in the same directory

Example output file name:
<Sib_18_30_symmetric_difference_results.csv_names.txt
"""
import sys, csv, os, argparse

def main(fName,column,dirName):
	#with open(dirName + fName, 'r') as reader:
	with open(dirName+ fName, 'r') as reader: 
		data = [row for row in csv.reader(reader)]

	#with open(dirName + fName + '_names.txt', 'w') as writer:
	with open(dirName+ fName + '_names.txt', 'w') as writer:
		count = 0
		for row in data:
			if (count != 0):
				writer.write(row[column] + '\n')
			count += 1
	print("Wrote", count, "rows")

 
#this function is used if you want to run on a directory
def runOnDir(dirName):
	filenames = next(os.walk(dirName))[2]
	for fName in filenames:
		#if ('DESeq2') in fName:     #commented line out in case file name does not have DESeq in name
			print("Running on file:", fName)
			main(fName, args.column, dirName)


if __name__ == "__main__":
	
	p = argparse.ArgumentParser(description="Extracts the first (on default), or a given column from a csv file. This will output a new text file with _name at the end.")
	p.add_argument('dir', nargs='?', help="The directory path")
	p.add_argument("-c", "--column", type =int, default=0, help="The column number (starting at 0) that you want to be extracted.")
	args = p.parse_args()
	if (args.dir[-1] != '/'):
		args.dir += '/'
	runOnDir(args.dir)
