#!/usr/bin/env python
"""
Script to add two count files together. Meant to add paired alignments 
and single alignments that originated from the same BAM file together 
after counting features using paired alignments and single alignments respectively. 

USAGE: python addCounts.py count_file_in_1 count_file_in_2 count_file_out
INPUT: count_file_in_1, count_file_in_2, count_file_out
OUTPUT: count_file_out

Written on 161228 by Ronald Cutler
Updated 170601: Uses floats instead of integers, skips first line if "Name" is in it.
"""
import sys

def addCounts(file1, file2, file3):

	with open (file1, 'r') as f1:
		names = []
		counts1 = []
		for line in f1:
			if "Name" in line:
				continue
			fields1 = line.split()
			names.append(fields1[0])
			counts1.append(fields1[1])
		counts1 = map(float, counts1) # converting strings to int. In py3: results = list(map(int, results))

	with open (file2, 'r') as f2:
		counts2 = []
		for line in f2:
			if "Name" in line:
				continue
			fields2 = line.split()
			counts2.append(fields2[1])
		counts2 = map(float, counts2) # converting strings to int

	with open (file3, 'w+') as f3:
		list_count = 0

		new_counts = [x + y for x, y in zip(counts1, counts2)] # adding each element of two list together 
		new_counts_int = map(int, new_counts) # convert float to int
		new_counts_str = map(str, new_counts_int) # convert back to string for writing to file 
		
		for i in names:
			f3.write(names[list_count])
			f3.write("\t")

			f3.write(new_counts_str[list_count])
			f3.write("\n")

			list_count += 1

if __name__ == "__main__":
	# take in 2 input files and path to output
	file1 = sys.argv[1]
	file2 = sys.argv[2]
	file3 = sys.argv[3]

	addCounts(file1, file2, file3)