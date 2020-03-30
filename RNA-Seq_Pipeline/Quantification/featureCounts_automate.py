#!/usr/bin/env python

"""
This assumes that featureCounts is installed and in the path environment
(can be run from the terminal).

This script runs featureCounts on a directory of name sorted BAM alignment files.
All output will be output to the given output directory.

USAGE: htseq-count_automate.py [options] -i <input_directory> -x <bam_suffix> -a <genome_annotation.gff3> -o <output_directory>
OUTPUT: htseq-count counts output file and htseq-count warnings file per alignment file in specified output directry

Updated 180704 by Ronald Cutler 
"""

import sys, os, datetime, time, multiprocessing, datetime
from glob import glob
from optparse import OptionParser
from functools import partial

__version__ = '1.0.0'

def featureCountsRun(inDir, bam_suffix, annot, output_dir, stranded, paired, idattr, feat_type, threads, overlap, fraction):
	# get bam files
    bam_suffix = "*" + bam_suffix
    matches = [y for x in os.walk(inDir) for y in glob(os.path.join(x[0], bam_suffix))]	

    # confirmation of files to run
    print("\nRunning on", len(matches), "files...")
    for files in matches:
        print(files)

    ####running featureCounts####
	
    # go into output dir
    os.chdir(output_dir)

    # check whether paired, overlap, or fraction flags exist
    if paired == True:
    	paired = "-p"
    else:
    	paired = ''

    if overlap == True:
    	overlap = "-O"
    else:
    	overlap = ''

    if fraction == True:
    	fraction = "--fraction"
    else:
    	fraction = ''

    for file in matches:
    	featureCountsRunSingle(file, annot, stranded, paired, idattr, feat_type, threads, overlap, fraction)

def featureCountsRunSingle(filename, annot, stranded, paired, idattr, feat_type, threads, overlap, fraction):
	"""Runs htseq-count on a single file as an instance"""

	# get only the filename for output
	output_file = filename.split("/")[len(filename.split("/")) - 1].rstrip(".bam") + "_counts.txt"
	
	# run htseq-count
	print('\nBegin analyzing: ' + filename)
	start = time.time()
	print('Command: featureCounts -a {0} -t {1} -g {2} -s {3} {4} -T {5} {6} {7} -o {8} {9}'.format(annot, feat_type, idattr, stranded, paired, threads, overlap, fraction, output_file, filename))
	os.system('featureCounts -a {0} -t {1} -g {2} -s {3} {4} -T {5} {6} {7} -o {8} {9}'.format(annot, feat_type, idattr, stranded, paired, threads, overlap, fraction, output_file, filename))
	end = time.time()
	print('Finished counting ' + output_file + ' in: ', (str(datetime.timedelta(seconds=(end-start)))))

def main():
	usage = "featureCounts_automate.py [options] -i <input_directory> -x <bam_suffix> -a <genome_annotation.gff3> -o <output_directory>\n"
	parser = OptionParser(usage, version="featureCounts_automate.py" + __version__)
	parser.add_option("-i", "--input-dir", action = "store", type = "string", dest = "input_dir", help = "Directory containing alignment files in BAM format.")
	parser.add_option("-x","--bam-suffix",action="store",type="string",dest="bam_suffix",help="Suffix of BAM files to be processed in input direectory. Make sure this is unique to only the ones you want to process. e.g. _sorted.bam")
	parser.add_option("-a", "--gene-annot", action = "store", type = "string", dest = "gene_annot_model", help = "Reference genome annotation in gff3 format.")
	parser.add_option("-o", "--output-dir", action = "store", type = "string", dest = "output_dir", help = "Output directory")
	parser.add_option("-s", "--stranded", action = "store", type = "int", dest = "stranded", help = "Whether the data is from a strand-specific assay. Specify the strandedness of the reads. Options are 0,  1, and 2 which correspond to unstranded Forward-Reverse and Reverse-Forward strandedness, respectively.", default = 0)
	parser.add_option("-p", "--paired", action = "store_true", dest = "paired", help = "Should be used when using paired reads. This counts fragments instead of reads (2 reads that make up a pair are counted as 1)")
	parser.add_option("-g", "--idattr", action = "store", type = "string", dest = "idattr", help = "GFF attribute to be used as feature ID (default, suitable for Ensembl GTF files: gene_id)", default = "gene_id")
	parser.add_option("-t", "--type", action = "store", type = "string", dest = "feat_type", help = "Feature type (3rd column in GFF file) to be used, all features of other type are ignored (default, suitable for Ensembl GTF files: exon)", default = "exon")
	parser.add_option("-T", "--threads", action = "store", type = "int", dest = "threads", help = "The number of threads we want to use. The amount of threads a machine has is determined using sysctl -n hw.ncpu", default = 1)
	parser.add_option("-O", "--overlap", action = "store_true", dest = "overlap", help = "Do not discard reads that overlap multiple features")
	parser.add_option("-f", "--fraction", action = "store_true", dest = "fraction", help = "Assign fractional counts where reads overlap multiple features where each overlapping feature will receive a fractional count of 1/y, where y is the total number of features overlapping with the read.")

	(options,args) = parser.parse_args()

	if not (options.input_dir and options.gene_annot_model and options.output_dir and options.bam_suffix):
		parser.print_help()
		sys.exit(0)
	if not os.path.exists(options.gene_annot_model):
		print('\n' + options.gene_annot_model + " does NOT exist" + '\n')
		sys.exit(0)
	if not os.path.exists(options.input_dir):
		print('\n' + options.input_dir + " does NOT exist" + '\n')
		sys.exit(0)
	if not os.path.exists(options.output_dir):
		print('\n' + options.output_dir + " does NOT exist" + '\n')
		sys.exit(0)
	else:
		featureCountsRun(options.input_dir, options.bam_suffix, options.gene_annot_model, options.output_dir, options.stranded, options.paired, options.idattr, options.feat_type, options.threads, options.overlap, options.fraction)

if __name__ == "__main__":
	main()