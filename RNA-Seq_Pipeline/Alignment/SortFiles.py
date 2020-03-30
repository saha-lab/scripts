#!/usr/bin/env python
import os, datetime, time, multiprocessing, sys
from functools import partial
"""
This script takes in a directory of .bam or .sam files and uses samtools to
automatically sort them all. Default is to sort by chromosome.

Updated 161223 by Ronald Cutler
Directory input is now taken in as the second argument in the command line

By Caroline Golino
"""
def getBamFiles(path, fileType):
	"""Gets all bam files from a given directory"""
	print ('Getting files')
	files = next(os.walk(path))[2]
	print ('Files to be sorted:')
	allFiles = []
	for f in files:
		if ('.'+fileType in f):
			allFiles.append(f)
			print(f)
	return allFiles

def sortFile(path, newPath, filename):
	"""Sorts a single file."""
	print('Begin sorting file: ' + filename)
	newName = newPath.replace(' ', '\ ')+filename + '_sorted.bam'
	start = time.time()
	os.system('samtools sort -@ 12 -o {0} {1}'.format(newName, path.replace(' ', '\ ')+filename))
	end = time.time()
	print('Finished '+filename+' ('+ str(end-start) +' seconds)')


def sortFiles(directory, fileType):
	allFiles = getBamFiles(directory, fileType)
	for f in allFiles:
		sortFile(directory, '-n', f)
	print ('Done sorting files.')

def sortFilesMultithread(directory, fileType):
	"""Sorts all of the files in a given directory"""
	allFiles = getBamFiles(directory, fileType)
	threadNum = multiprocessing.cpu_count()

	newPath = directory+'Sorted_bam_files_'+str(datetime.date.today())+ '/'
	os.makedirs(newPath)
	os.chdir(newPath)

	runSorts = partial (sortFile, directory, newPath)

	print('Begin sorting files')
	pool = multiprocessing.Pool(processes=threadNum)
	pool.map(runSorts, allFiles)
	pool.close()
	pool.join()

if __name__ == "__main__":
	directory = sys.argv[1]
	sortFilesMultithread(directory + '/', "bam")
