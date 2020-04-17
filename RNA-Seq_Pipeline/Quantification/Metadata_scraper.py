#!/usr/bin/env python3
#
# Metadata_scraper.py
#
# LAST EDIT: 2020-04-13
#
# This script searches a metadata folder for an abundance file to give a
# DESeq2 formatted count file: "genename|XB-geneID     count#"
# if there is no avaiable XB-gene ID, then the genename is copied twice.

import pandas
import sys, csv, os, argparse
import numpy as np

def metadata_extract(file, col1, col2, col3):
    #Open the file
    with open(file) as file1:
        filereader = pandas.read_csv(file1, sep = '\t') #Read this into a data frame
        num_gene_xen = filereader[[col1, col2, col3]]
    return num_gene_xen

def tsv_file(tsv_file, col1, col2): #Output a dictionary with 'gene + number' key and 'EST count' IDs
    with open(tsv_file) as file:
        filereader1 = pandas.read_csv(tsv_file, sep = '\t')
        id_estcounts = filereader1[[col1, col2]] #columns we want
        t_id = id_estcounts[col1].str.split('|') #target id list generation
        gene_keys = []
        for i in t_id:
            gene_keys.append(i[1]) #extract gene name
        EST_series = id_estcounts[col2]
        est_values = []
        for j in EST_series:
            est_values.append(j) #extract est id
        gene_est = dict(zip(gene_keys, est_values)) #zip both gene names and est ids
    return gene_est

##### MAIN #####

#stop printing unnecessary warnings
pandas.options.mode.chained_assignment = None

p = argparse.ArgumentParser(description="Will take an abundance and the metadata file.")
p.add_argument('abundance', nargs='?', help="The abundance or kallisto output file")
p.add_argument('metadata', nargs='?', help="The metadata geneinfo file (.txt format)")
args = p.parse_args()

df = metadata_extract(args.metadata, 'Number', 'Genename', 'Xenbase_ID')
df_genenames = df['Genename'] #Genename series
df_xenbaseids = df['Xenbase_ID'] #Xenbase ID series
df_genenumber = df['Number'] #Gene+number series

genedict = tsv_file(args.abundance, 'target_id', 'est_counts')

#Gene lists

gene_namelist = []
for i in df_genenames:
    gene_namelist.append(i)
#gene_namelist
gene_nameseries = pandas.Series(gene_namelist)

#Xenbase id lists
xenid_list = []
for j in df_xenbaseids:
    xenid_list.append(j)
#xenid_list
xenid_series = pandas.Series(xenid_list)

#number series lists
number_list = []
for i in df_genenumber:
    if i not in genedict.keys():
        number_list.append('N/A')
    else:
        number_list.append(genedict[i])
#number_list
number_series = pandas.Series(number_list)

final_frame = pandas.concat([gene_nameseries, xenid_series, number_series], axis = 1)
final_frame.columns = ['Gene Name', 'XenBase ID', 'EST count']
final_frame.loc[final_frame['XenBase ID'].isna(),'XenBase ID'] = final_frame['Gene Name']

final_frame["GeneName|ID"] = final_frame["Gene Name"].astype(str) +"|" + final_frame["XenBase ID"]

output_frame = final_frame[['GeneName|ID', 'EST count']]
output_frame[("EST count")] = output_frame[("EST count")].replace("N/A", 0.0)
output_frame[("EST count")] = output_frame[("EST count")].round(0).astype(int)

#making outputfile path
l = str(args.abundance)
l = l.split('/')
parentname =l[-2] 

outputfile = args.abundance[:-13] + parentname+ '.txt'

output_frame.to_csv(outputfile, sep='\t', index=False, header = False)
