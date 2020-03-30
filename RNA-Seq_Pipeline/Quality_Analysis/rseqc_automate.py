#!/usr/bin/env python

"""
This assumes that RSeQC is installed and the modules within this package are in
the PATH environment (can be run from the terminal).

This script recursively get all of the bam files from the current directory and
any subdirectories and then runs various modules from RSeQC in order to perform
alignment file quality analysis.

This runs the following RSeQC modules:
deletion_profile.py
insertion_profile.py
mismatch_profile.py
junction_annotation.py
junction_saturation.py
read_distribution.py

USAGE: rseqc_automate.py -i <input_directory> -x <bam_suffix> -a <genome_annotation.bed> -r <read_leangth> -p <read_pairing>
Output: RSeQC module outputs for each bam in a directories following the naming
scheme, [input_bam]_RSeQC

Updated 180311 by Ronald Cutler
TODO: Parallelize this process to run multiple instances of RSeQC modules
"""
import sys, os
from glob import glob
from optparse import OptionParser

__version__ = '1.0.0'

def modulesRun(inDir, annot, readLen, paired, bam_suffix):
    # get bam files
    bam_suffix = "*" + bam_suffix
    matches = [y for x in os.walk(inDir) for y in glob(os.path.join(x[0], bam_suffix))]

    # confirmation of files to run
    print("\nRunning on", len(matches), "files...")
    for files in matches:
        print(files)

    # running RSeQC modules on each file
    for files in matches:

        print("\nProcessing:", files)

        # create an outputDir for this alignment
        outdir = files[:-4] + "_RSeQC/"
        try:
            os.makedirs(outdir)
            print("Ouput Folder:", outdir, "\n")
        except FileExistsError:
            print("\nThe output folder:", outdir, "already exist! Please make sure that this is not being overwritten!\n")

        # setting output prefix as input file name
        outPrefix = outdir + files.split('/')[len(files.split('/')) - 1]

        # running deletion_profile.py module
        print("Calculating deletion profile...")
        os.system('deletion_profile.py -i {0} -l {1} -o {2}'.format(files, readLen, outPrefix))

        # running insertion_profile.py module
        print("\nCalculating insertion profile...")
        os.system('insertion_profile.py -i {0} -s {1} -o {2}'.format(files, paired, outPrefix))

        # running mismatch_profile.py module
        print("\nCalculating mismatch profile...")
        os.system('mismatch_profile.py -i {0} -l {1} -o {2}'.format(files, readLen, outPrefix))

        # running junction_annotation.py module
        print("\nCalculating splicing rates...")
        os.system('junction_annotation.py -i {0} -r {1} -o {2}'.format(files, annot, outPrefix))

        # running junction_saturation.py module
        print("\nCalculating splicing saturation...")
        os.system('junction_saturation.py -i {0} -r {1} -o {2}'.format(files, annot, outPrefix))

        # running read_distribution.py module
        outputText = outPrefix + ".read_distribution.txt"
        print("\nCalculating read distribution...")
        os.system('read_distribution.py -i {0} -r {1} | tee '.format(files, annot, outputText))

def main():
    # parser user interface with required input parameters
    usage="rseqc_automate.py -i <input_directory> -x <bam_suffix> -a <genome_annotation.bed> -r <read_leangth> -p <read_pairing>\n"
    parser = OptionParser(usage,version="rseqc_automate.py" + __version__)
    parser.add_option("-i","--input-dir",action="store",type="string",dest="input_dir",help="Directory continaing alignment files in BAM format.")
    parser.add_option("-x","--bam-suffix",action="store",type="string",dest="bam_suffix",help="Suffix of BAM files to be processed in input direectory. Make sure this is unique to only the ones you want to process. e.g. _sorted.bam")
    parser.add_option("-a","--gene-annot",action="store",type="string",dest="gene_annot_model",help="Reference gene annotation in bed format. This file is better to be a pooled gene model as it will be used to annotate splicing junctions [required]")
    parser.add_option("-r","--read-length",action="store",type="int",dest="read_len", help="Read length")
    parser.add_option("-p","--read-pairing",action="store",type="string",dest="read_pair",help="\"SE\"(single-end) or \"PE\"(pair-end).")

    (options,args)=parser.parse_args()

    if not (options.input_dir and options.gene_annot_model and options.read_len and options.read_pair):
        parser.print_help()
        sys.exit(0)
    if not os.path.exists(options.gene_annot_model):
        print('\n' + options.gene_annot_model + " does NOT exist" + '\n')
        sys.exit(0)
    if os.path.exists(options.input_dir):
        modulesRun(options.input_dir, options.gene_annot_model, options.read_len, options.read_pair, options.bam_suffix)
    else:
        print('\n' + options.input_dir + " does NOT exist" + '\n')
        sys.exit(0)

if __name__ == "__main__":
    main()
