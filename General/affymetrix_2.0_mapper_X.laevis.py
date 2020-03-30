#!/usr/bin/env python
"""
Mapping Affymetric 2.0 probe names to xenbase gene names.
Mapping file downloaded at: ftp://ftp.xenbase.org/pub/GenePageReports/GenePageAffymetrix_laevis2.0.txt

Mapping file is a csv file with the gene name in first column and probe name in
the second column. The input file is a text file with probe Affymetric 2.0 probe names on each line.

USAGE: affymetrix_2.0_mapper_X.laevis.py <mapping.txt> <probe_names_input.txt>

Update 180627 by Ronald Cutler
"""
import sys, os

def main(mapping, input):
    # read in mapping as dict where the probe names are stored as keys
    # for genes with multiple probes, created a spearate entry for each probe
    map_dict = {}
    with open(mapping, 'r') as map:
        for line in map:
            #print(line)
            if ',"' in line: # multiple probe name entries
                split = line.split(",")
                gene_name = split[0]
                split.pop(0)
                #print(split)
                for probe in split:
                    probe = probe.lstrip('"').rstrip('"\n')
                    map_dict[probe] = gene_name
            else: # just one probe name entry
                split = line.split(",")
                map_dict[split[1].rstrip("\n")] = split[0]

    # read in input and map the probes to the input to create a new list of names
    # in the same order as the input
    output_names = []
    no_key_count = 0
    with open(input, 'r') as _input:
        for line in _input:
            line = line.rstrip("\n").lower()
            #print(line)
            if map_dict.get(line) != None:
                output_names.append(map_dict.get(line))
            else:
                no_key_count += 1
                output_names.append("NA")
    print("Total keys not found =", no_key_count)

    # write the output to a new text file
    with open(input[:-4] + "_gene_names.txt", 'w') as out:
        for line in output_names:
            out.write(line + "\n")

if __name__ == "__main__":
  main(sys.argv[1], sys.argv[2])
