"""
Converts gene annotations in GFF format to GTF format 
Accounts for one isoform/gene in the GFF file

Usage: python GFF_to_GTF_isoform.py <inFile> <outFile>

INPUT: GFF file with isoforms
OUTPUT: GTF file

Written by Ronald Cutler
"""
import sys


infile = open(sys.argv[1],'r')
outfile = open(sys.argv[2],'w')

gene=''
nE=0
nT=0 # Give transcripts with same name, specific names
transcript=''

for line in infile:
    if line.startswith('chr'):
        if line.split('\t')[2]=='exon': #only take lines for exons
            if line.split('\t')[8].strip('mRNA ').strip('exon ').strip(';\n')==transcript: # Another exon of the same gene? 
                nE+=1
                outfile.writelines('\t'.join(['\t'.join(line.split('\t')[:8]),';'.join([' '.join([' gene_id', '"'+transcript+'"']), ' '.join([' transcript_id', '"'+transcript+'"']), ' '.join([' exon_number', '"'+str(nE)+'"'+';'])])])+'\n')            
            else:
                transcript=line.split('\t')[8].strip('mRNA ').strip('exon ').strip(';\n') # New gene
                nE=1
                outfile.writelines('\t'.join(['\t'.join(line.split('\t')[:8]),';'.join([' '.join([' gene_id', '"'+transcript+'"']), ' '.join([' transcript_id', '"'+transcript+'"']), ' '.join([' exon_number', '"'+str(nE)+'"'+';'])])])+'\n')

    
outfile.close()
infile.close()