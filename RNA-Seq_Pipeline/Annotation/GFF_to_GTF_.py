"""
Converts gene annotations in GFF format to GTF format

Usage: python GFF_to_GTF.py <inFile> <outFile>

INPUT: GFF file
OUTPUT: GTF file

Written by Ronald Cutler
"""
import sys

inFile = open(sys.argv[1],'r')
outFile = open(sys.argv[2], 'w')

for line in inFile:
  #skip comment lines that start with the '#' character
  if line[0] != '#':
    #split line into columns by tab
    data = line.strip().split('\t')

    ID = ''

    #if the feature is a gene 
    if data[2] == "gene":
      #get the id
      ID = data[-1].split('ID=')[-1].split(';')[0]

    #if the feature is anything else
    else:
      # get the parent as the ID
      ID = data[-1].split('Parent=')[-1].split(';')[0]
    
    #modify the last column
    data[-1] = 'gene_id "' + ID + '"; transcript_id "' + ID

    #print out this new GTF line
    outFile.write('\t'.join(data))

inFile.close()
outFile.close()