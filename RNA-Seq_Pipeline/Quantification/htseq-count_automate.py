#!/usr/bin/env python

"""
This assumes that HTSeq-count is installed and in the path environment
(can be run from the terminal).

This script run HTSeq-count on a directory of name sorted BAM alignment files.
Since HTSeq-count only uses 1 thread per process, this script runs multiple
instances of HTSeq-count on each file. The maximum number of instances run is equal to 
the number of threads on the machine. All output will be output to the given output directory.

USAGE: htseq-count_automate.py [options] -i <input_directory> -x <bam_suffix> -a <genome_annotation.gff3> -o <output_directory>
OUTPUT: htseq-count counts output file and htseq-count warnings file per alignment file in specified output directry

Updated 180327 by Ronald Cutler 
"""

import sys, os, datetime, time, multiprocessing, datetime
from glob import glob
from optparse import OptionParser
from functools import partial

__version__ = '1.0.0'

def htseqCountRun(inDir, bam_suffix, annot, output_dir, align_format, stranded, idattr, feat_type):
	# get bam files
    bam_suffix = "*" + bam_suffix
    matches = [y for x in os.walk(inDir) for y in glob(os.path.join(x[0], bam_suffix))]	

    # confirmation of files to run
    print("\nRunning on", len(matches), "files...")
    for files in matches:
        print(files)

    ####running htseq####

    # go into output dir
    os.chdir(output_dir)

    # get thread number
    threadNum = multiprocessing.cpu_count()
    
    # make a new version of the htseqCountRunSingle with arguments alrready filled in that will be constant for all files run on
    runHTSeq = partial(htseqCountRunSingle, annot = annot, align_format = align_format, stranded = stranded, idattr = idattr, feat_type = feat_type)

    # runnning multiple instances of htseq-count on all files
    pool = multiprocessing.Pool(processes=threadNum)
    pool.map(runHTSeq, matches)
    pool.close()
    pool.join()

def htseqCountRunSingle(filename, annot, align_format, stranded, idattr, feat_type):
	"""Runs htseq-count on a single file as an instance"""

	# get only the filename for output
	output_file = filename.split("/")[len(filename.split("/")) - 1].rstrip(".bam")
	
	# run htseq-count
	print('\nBegin analyzing: ' + filename)
	start = time.time()
	print('Command: htseq-count -f {0} -s {1} -i {2} -t {3} {4} {5} >{6}_htseq_out.txt 2>{6}_htseq_out_WARNINGS.txt'.format(align_format, stranded, idattr, feat_type, filename, annot, output_file))
	os.system('htseq-count -f {0} -s {1} -i {2} -t {3} {4} {5} >{6}_htseq_out.txt 2>{6}_htseq_out_WARNINGS.txt'.format(align_format, stranded, idattr, feat_type, filename, annot, output_file))
	end = time.time()
	print('Finished counting ' + output_file + ' in: ', (str(datetime.timedelta(seconds=(end-start)))))

def main():
	usage = "htseq-count_automate.py [options] -i <input_directory> -x <bam_suffix> -a <genome_annotation.gff3> -o <output_directory>\n"
	parser = OptionParser(usage, version="htseq-count_automate.py" + __version__)
	parser.add_option("-i", "--input-dir", action = "store", type = "string", dest = "input_dir", help = "Directory containing alignment files in BAM format.")
	parser.add_option("-x","--bam-suffix",action="store",type="string",dest="bam_suffix",help="Suffix of BAM files to be processed in input direectory. Make sure this is unique to only the ones you want to process. e.g. _sorted.bam")
	parser.add_option("-a", "--gene-annot", action = "store", type = "string", dest = "gene_annot_model", help = "Reference genome annotation in gff3 format.")
	parser.add_option("-o", "--output-dir", action = "store", type = "string", dest = "output_dir", help = "Output directory")
	parser.add_option("-f", "--format", action = "store", type = "string", dest = "align_format", help = "type of <alignment_file> data, either 'sam' or 'bam' (default: sam)", default= "sam")
	parser.add_option("-s", "--stranded", action = "store", type = "string", dest = "stranded", help = "whether the data is from a strand-specific assay .Specify 'yes', 'no', or 'reverse' (default: yes). 'reverse' means 'yes' with reversed strand", default = "yes")
	parser.add_option("-d", "--idattr", action = "store", type = "string", dest = "idattr", help = "GFF attribute to be used as feature ID (default, suitable for Ensembl GTF files: gene_id)", default = "gene_id")
	parser.add_option("-t", "--type", action = "store", type = "string", dest = "feat_type", help = "feature type (3rd column in GFF file) to be used, all features of other type are ignored (default, suitable for Ensembl GTF files: exon)", default = "exon")

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
		htseqCountRun(options.input_dir, options.bam_suffix, options.gene_annot_model, options.output_dir, options.align_format, options.stranded, options.idattr, options.feat_type)

if __name__ == "__main__":
	main()