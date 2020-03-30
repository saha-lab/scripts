#!/bin/bash
## interleave two paired-end fastq files
## USAGE: interleave_fastq.sh <r1.fastq> <r2.fastq> <output.fastq>
## Updated 180721 by Ronald Cutler
reads1=$1
reads2=$2
out=$3

paste <(paste - - - - < $reads1) \
      <(paste - - - - < $reads2) \
    | tr '\t' '\n' \
    > $out