#!/bin/bash
## separates an interleaved fastq into two paired-end fastq files given that paired end reads are sorted properly
## USAGE: decouple_fastq.sh <reads-int.fastq>
## Updated 180703 by Ronald Cutler 
readsint=$1
reads1=$readsint
reads1+="_1.fastq"
reads2=$readsint
reads2+="_2.fastq"
paste - - - - - - - - < $readsint \
    | tee >(cut -f 1-4 | tr '\t' '\n' > $reads1) \
    | cut -f 5-8 | tr '\t' '\n' > $reads2