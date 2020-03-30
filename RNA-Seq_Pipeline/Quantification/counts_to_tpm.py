#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Takes in a directory of HTSeq-count output files and a file
with gene names and their corresponding lengths to produce 
a count file with transcripts per million (tpm) counts for 
each gene. This would be for comparing identical genes across samples

Uses formula described here: https://www.ncbi.nlm.nih.gov/pubmed/22872506
TPM = ((tag count for transcript n) / length of transcript n) * 1million / normalizing term

Last updated 170328 by Ronald Cutler

USAGE: counts_to_tpm.py
Output: Directory of tpm count files corresponding to HTSeq-count input directory files
"""

import csv, sys, os
from itertools import izip

def tpm_counter(input_dir, count_file, gene_length_file, output_dir):
	"""Converts absolute counts to tpm"""
	
	counts = open(count_file, 'r')
	gene_lengths = open(gene_length_file, 'r')


	rpk_list = []
	tpm_list = []
	name_list = []
	total_rpk = 0

	for count_line, gene_length_line in izip(counts, gene_lengths):
		count_data = count_line.strip().split('\t')
		gene_length_data = gene_length_line.strip().split('\t')

		if count_data[0] == gene_length_data[0]:
			kilobase = float(gene_length_data[1])/float(1000)
			rpk = float(count_data[1]) / kilobase
			total_rpk += rpk
			rpk_list.append(rpk)
			#print "RPK: ", rpk

			name_list.append(count_data[0])

	#print "TOTAL RPK: ", total_rpk

	per_million_scaling_factor = float(total_rpk) / float(1000000)

	#print "PER MILL SCALE FACTOR: ", per_million_scaling_factor


	for rpk in rpk_list:
		tpm = rpk/per_million_scaling_factor
		tpm_list.append(int(tpm))

	with open(output_dir + count_file.replace(input_dir, '') + "_tpm_count.txt", 'wb') as f:
		writer = csv.writer(f, delimiter = '\t')
		writer.writerows(izip(name_list, tpm_list))

	counts.close()
	gene_lengths.close()


def getInput():
	userInput = []
	path = raw_input('What is the path to the folder containing the HTSeq-count output files?\n')#.rstrip()
	userInput.append(path)

	files = [os.path.join(root, name) 
			 for root, dirs, files in os.walk(path)
			 for name in files]
	userInput.append(files)

	userInput.append(raw_input("What is the file containing gene lengths?\n"))

	path = raw_input('Where would you like to save your output files?\n')#.rstrip()
	if (path[-1] != '/'):
		path+='/'
	userInput.append(path)

	return userInput

def main():
	userInput = getInput()
	print('List of files being run through:')
	for file in userInput[1]:
		print file 

	for file in userInput[1]:
		tpm_counter(userInput[0], file, userInput[2], userInput[3])

if __name__ == '__main__':
	main()




