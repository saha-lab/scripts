#!/usr/bin/perl
# Ace file format (https://en.wikipedia.org/wiki/ACE_(genomic_file_format)) 
# output by Consed to fasta converter
# USAGE: aceConvert.pl <in.ace> <out.fasta>
# Updated 180721 by Ronald Cutler

use strict;
use warnings;


my $infile = $ARGV[0];
my $outfile = $ARGV[1];

open INPUT, $infile or die $!;
open OUTPUT, ">$outfile" or die $!;

my $waitForHeader = 1;

while (my $line = <INPUT>) {
    if ($waitForHeader) {
        if ($line=~"^CO") {
            my @splitter = split (" ",$line);
            print OUTPUT ">"."$splitter[1]\n";
            $waitForHeader = 0;
        }
        else {
            next;
        }
    }
    else {
        if ($line=~"^BQ") {
            $waitForHeader=1;
        }
        else {
            unless ($line eq "\n") {
                $line=~s/\*/-/g;
                print OUTPUT $line;
            }    
        }
    }
}

close INPUT;
close OUTPUT;