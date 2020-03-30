Updated 180506 by Ronald Cutler

————————————————————————
add_gene_descriptions.py
————————————————————————
Add gene descriptions to a list of genes output by DESeq2 using a tab-delimmated mapping file of gene names and their descriptions

——————————————————————
shared_finder_three.py
——————————————————————
Find the shared genes between 3 SDE trimmed DESEq2 output files 

——————————————————————————————
shared_finder_two_collapsed.py
——————————————————————————————
Find the shared genes between 2 SDE trimmed DESEq2 output files where homeologs were collapsed into a single gene

————————————————————
shared_finder_two.py
————————————————————
Find the shared genes between 2 SDE trimmed DESEq2 output files 

———————————————————————
shared_finder_unique.py
———————————————————————
Find the shared genes between the two outputs of unique_finder_two.py

——————————————————————
shared_gene_FC_diff.py
——————————————————————
In a directory of outputs from shared_finder_two.py, find genes where the fold change is different between the two origin comparisons

—————————————
TPM_salmon.py
—————————————
Create new cvs files with gene name and TPM from a directory of salmon quant files

———————————
trim_SDE.py
———————————
Takes a deseq2 output file ranked by padj values and filters out all genes with padj > 0.05

—————————————————————————
unique_finder_collapse.py
—————————————————————————
Get the unique genes between two DESeq2 outputs where homeologs were collapsed

——————————————————————
unique_finder_three.py
——————————————————————


————————————————
unique_finder_two.py
————————————————
