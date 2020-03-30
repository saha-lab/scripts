#!/usr/bin/env python
"""
Takes in a .seq file containing the 'feature table' annotation
output from DNAMaster, and converts it into a .gff3 annotation file.

USAGE: DNAMaster_to_gff3.py <in.seq>

Written by Caroline Golino, updated by Ronald Cutler 180521
"""
import sys

def scan_lines(lines):
	"""Returns a list of lists containing information for each gene."""
	allGenes = []
	gene = [] #start, end, direction, gp number, function
	for line in lines:
		if (line == "\n"): # accounting for two \n symbols between each entry
			allGenes.append(gene)
			gene = []
		else:
			gene.extend(parse_line(line))
	allGenes.append(gene)
	return allGenes

def parse_line(line):
	"""Parses the contents of a line from DNA-Master output."""
	info = []
	if ("CDS" in line):
		complement = ("complement" in line)
		if (complement):
			start = line[line.find("(")+1:line.find(" -")]
			end = line[line.find("- ")+2:-2]
		else:
			start = line[4:line.find(" -")]
			end = line[line.find("- ")+2:line.find("\n")]
		info = [start, end, complement]
	elif ("note=F:" in line):
		function = line[line.find("note=F: ")+8:line.find("\n")]
		info = [function]
	elif ("product=" in line):
		if "tRNA" in line: # do not include tRNA
			return info
		number = line[line.find("product=\"")+9:-2]
		info = [number]
	return info

def convert2gff(allGenes):
	"""Returns the info from each gene formatted as lines in a .gff3 file."""
	newLines = []
	for gene in allGenes:
		print("GENE: "+ str(gene))
		if not gene:
			continue
		line = "HerbertWM\tDNA-Master\tCDS\t"+gene[0]+"\t"+gene[1]+"\t.\t"
		if gene[2]:
			line += "-\t.\t"
		else:
			line += "+\t.\t"
		try: 
			line += "product=\""+gene[3]+"_"+gene[4].replace(" ", "_") + "\"\n"
		except IndexError:
			line += "product=\""+gene[3] + "\"\n"
		newLines.append(line)

	return newLines

def write_file(dnamFile, lines):
	"""Simply writes the generated lines as a .gff3 file."""
	f = open(dnamFile[:-3] + "gff3", "w")
	f.writelines(lines)
	f.close()

def main(dnamFile):
	with open(dnamFile, "rU", encoding="latin-1") as f:
		lines = f.readlines()
	allGenes = scan_lines(lines)
	print(allGenes)
	lines = convert2gff(allGenes)
	write_file(dnamFile, lines)

if __name__ == "__main__":
	main(sys.argv[1])