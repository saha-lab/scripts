#!/usr/bin/env perl
"""
Retrieves fasta sequences from fasta master file using names from a text file. 

Usage: extract_fasta_entries.pl <list_of_names.txt> <master_sequences.fasta> <output_sequences.fasta>

Updated 180721 by Ronald Cutler
"""
my $list_file = $ARGV[0];
my $fasta_in = $ARGV[1];
my $fasta_out = $ARGV[2];
open(LIST_FILE, "<", $list_file) or die "could not open '$list_file' : $! \n";
open(FASTA_IN, "<", $fasta_in) or die "could not open '$fasta_in' : $! \n";
open(FASTA_OUT, ">", $fasta_out) or die "could not open $fasta_out : $! \n";
my @headers = ();
while(<LIST_FILE>) {
    chomp;
    next if ( /^\s*$/ );
    push(@headers, $_);
}
my $pat = join '|', map quotemeta, @headers;
$/ = ">";
while(<FASTA_IN>) {
    chomp;
    if ( /$pat/ ) { print FASTA_OUT ">$_"; }
}
close(LIST_FILE);
close(FASTA_IN);
close(FASTA_OUT);