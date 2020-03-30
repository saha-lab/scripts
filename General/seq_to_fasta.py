
#!/usr/bin/env python
"""
Converts .seq files in a directory output from CLC to fasta files.
Why not just export CLC files as fasta?

USAGE: seq_to_fasta.py <path_to_input_dir>

Updated 180721 by Ronald Cutler
"""
import os, sys

def getSequences(path):

	#print('uh were in a method...')
	seqFiles = []

	# sequences will store tuples of (nameOfTheFile, sequence)
	sequences = []

	for filename in os.listdir(path):
		if filename.endswith('.seq'):
			seqFiles.append(filename)

	for seq in seqFiles:
		sFile = open(path+'/'+seq, 'r')
		fName = seq[seq.rfind('/')+1:]
		sequences.append((fName, sFile.read()))
		sFile.close()

	return sequences

def makeFASTA(sequences, path):
	f = open(path[:-4] + ".fasta", 'wb')

	for item in sequences:
		f.write(">"+item[0]+'\n')
		thing = item[1]

		lines = []

		for line in thing.splitlines():
		    line = line.strip()
		    lines.append(line)

		for line in lines:
			f.write(line+'\n')
	f.close()

if __name__ == "__main__":
	makeFASTA(getSequences(sys.argv[1]))