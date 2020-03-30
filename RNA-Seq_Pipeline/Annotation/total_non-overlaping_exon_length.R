# A script taken from: https://www.biostars.org/p/83901/
# Getting the total non-overlapping exon length per gene for usage in getting FPKM/TPM counts from abosulte counts contained in HTSeq-count output files
# Using the GenomicFeatures R package
# Input: GTF File

# First, import the GTF-file that you have also used as input for htseq-count
library(GenomicFeatures)
txdb <- makeTxDbFromGFF("yourFile.gtf",format="gtf")
# then collect the exons per gene id
exons.list.per.gene <- exonsBy(txdb,by="gene")
# then for each gene, reduce all the exons to a set of non overlapping exons, calculate their lengths (widths) and sum then
exonic.gene.sizes <- lapply(exons.list.per.gene,function(x){sum(width(reduce(x)))})