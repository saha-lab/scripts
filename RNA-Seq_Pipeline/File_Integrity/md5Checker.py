#!/usr/bin/env python
"""
Checks if two given md5 checksums are equivilent. Give the folder containing fastq files and 
the corresponding folder containing md5 files. Runs "md5 <fastqIn> from terminal and comapares to 
supplied md5 in file.

USAGE: md5Checker.py 

Update 180611 by Ronald Cutler
"""
import sys, subprocess, os

def checker( fastqIn, md5file ):

	print ("FASTQ:", fastqIn)
	print ("MD5:", md5file)
	proc = subprocess.check_output(["/sbin/md5", fastqIn])
	proc = str(proc).split('= ')[1][:-3]
	print("\nNew md5:\t", proc)

	with open( md5file, 'r' ) as reader:
		md5file_line = ""
		for line in reader:
			md5file_line = line.split(" ")[0]
			print ("Downloaded md5:\t", md5file_line)
		if proc == md5file_line:
			print ("\nTrue, file downloaded successfully!\n")
		else:
			print ("\nFalse, re-check new md5 or re-download fastq file!\n")
			sys.exit()

def main(fastqFolder_path, fastqFolder, md5Folder_path, md5Folder ):
	print ("\nStarting checking process...\n")
	for fastq_file, md5_file in zip(fastqFolder, md5Folder):
		checker(fastqFolder_path + fastq_file, md5Folder_path + md5_file)


def userInput():
	userInput = [] #[path to fastq folder, [list of .fastq.gz], path to md5 folder, [list of .md5]]
	fastq_path = input("Path to fastq.gz or tar.gz containing folder\n").rstrip(" ")
	if (fastq_path[-1] != '/'):
		fastq_path+='/'
	userInput.append(fastq_path)
	userInput.append(next(os.walk(fastq_path))[2]) #Appending all files
	

	md5_path = input("Path to md5 containing folder \n").rstrip(" ")
	if (md5_path[-1] != '/'):
		md5_path+='/'
	userInput.append(md5_path)
	userInput.append(next(os.walk(md5_path))[2]) #Appending all files

	return userInput

if __name__ == "__main__":
	input_folders = userInput()
	for file in input_folders[1]:
		print(file)
		if (".gz" not in file):
			input_folders[1].remove(file)
	for file in input_folders[3]:
		print(file)
		if (".md5" not in file):
			input_folders[3].remove(file)

	if len(input_folders[1]) != len(input_folders[3]):
		print ("\nUneven amount of fastq.gz and md5 files. Please check the folders.\n")
		exit()

	input_folders[1] = sorted(input_folders[1], key=str.lower)
	input_folders[3] = sorted(input_folders[3], key=str.lower)


	main(input_folders[0], input_folders[1], input_folders[2], input_folders[3])