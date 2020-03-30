# Generates plots of the expression of each gene over time.
# Input a .csv file with read counts or RPKM (or whatever value you'd like).
# Each row should represent a given gene of interest.
# Each column should be a different timepoint, with the columns in order.
# The column names must contain a number indicating its time point.
# Ex: columns titled 'T0', 'T5', 'T15'
# Make sure that the only numbers in the column titles are its time!
# Ex: Do NOT have columns 'T0_Replicate1', 'T0_Replicate2', 'T5_Replicate1'
# If you have multiple replicates, you must merge them so that there is
#  only one column per timepoint (such as by taking the mean of the replicates).
#
# To run:
# Open r in command line with the working directory the folder of this script.
# Enter the following in the R command line:
#   source("ReadCountPlotter.R")
# Run this script:
#   PlotReads(countFile, xlabel, ylabel)
# Where countFile is the path to the .csv file as described above,
#   xlabel is the label of the x axis for the plots (ex: 'Time (minutes)')
#   and ylabel is the label of the y axis (ex: 'Mean RPMK' or 'Mean Read Counts')
#
# Example run of the script:
#   source("ReadCountPlotter.R")
#   PlotReads('/Volumes/cachannel/RNA_SEQ/countFile.csv', 'Time (hours)', 'Mean RPKM')
#
# Written by Caroline Golino and John Marken
# Updated 170504

PlotReads <- function(countFile, xlabel, ylabel){

  closeAllConnections()
  rm(list=ls())

  counts = read.csv(file=countFile, head=TRUE, sep=',')

  wrap_strings <- function(stringVec,width){as.character(sapply(stringVec, FUN=function(x){paste(strwrap(x,width=width),collapse="\n")}))}

  geneNames <- gsub("_"," ",counts[,1])
  geneNames <- wrap_strings(geneNames, width=40)

  outFilename = paste(countFile, 'plots.pdf', sep='_')

  entries_list = list()

  numGenes = nrow(counts)

  timepoints = gsub('[^0-9]', '', colnames(counts))
  timepoints = timepoints[-1]
  timepoints = unlist(lapply(timepoints, strtoi))

  pdf(file = outFilename)

  for( ii in 1:numGenes){
    if( (ii-1) %% 4 == 0){
      par(mfrow = c(2,2))
      plot(timepoints, counts[ii,2:(length(timepoints)+1)], main = geneNames[ii], xlab = xlabel, ylab = ylabel, cex.main=0.75)
      lines(timepoints, counts[ii,2:(length(timepoints)+1)])
    }
    else{
      plot(timepoints, counts[ii,2:(length(timepoints)+1)], main = geneNames[ii], xlab = xlabel, ylab = ylabel, cex.main=0.75)
      lines(timepoints, counts[ii,2:(length(timepoints)+1)])    
    }
  }

  dev.off()
}