

file_len<- read.delim("/Volumes/CaChannel/RNA_SEQ/Reference_Genomes/9.1_Reference_Files/XENLA_UTAmayball_cdna_longest_CHRS2_gene_lengths.txt",header=F,sep="\t")
file_count<- read.delim("/Volumes/CaChannel/RNA_SEQ/APRotations/161221_Hisat2/HTSeq-count/S18_11C/160716_S18_11C_1.bam_sorted.bam_htseq_out.txt",header=F,sep="\t")
colnames(file_len)<- c("GeneName","Len")
colnames(file_count)<- c("GeneName","Count")  
file_count<-file_count[ !grepl("__", file_count$GeneName) ,]
total_count<- sum(file_count$Count)
oneB<-10^9
finallist <- merge(file_len,file_count,by="GeneName")
finallist$RPKM<-0
finallist[,2:4] <- (sapply(finallist[,2:4], as.double))
finallist$RPKM<- (oneB*finallist$Count)/(total_count*finallist$Len)
#finallist<-finallist[finallist$RPKM>1,]
write.table(finallist,file="rpkm.txt",sep="\t", col.names = T, row.names = F)