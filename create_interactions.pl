#!/usr/bin/perl

use strict;

my %hash;
open(F,"WF");
while(<F>){
	my $line = $_;
	$line =~s/\n//g;$line =~s/\n//g;
	my ($name,$r) = split(/\t/,$line);
	my $resistance;
	if ($r =~/R/){$resistance = "R";}
	elsif ($r =~/S/){$resistance = "S";}
	else{$resistance = "MR";}
	$hash{$name}{"White fly"} = $resistance;
}
close(F);

open(G,"GR");
while(<G>){
        my $line = $_;
        $line =~s/\n//g;$line =~s/\n//g;
        my ($name,$r) = split(/\t/,$line);
        my $resistance;
        if ($r =~/R/){$resistance = "R";}
        elsif ($r =~/S/){$resistance = "S";}
        else{$resistance = "MR";}
        $hash{$name}{"Green mite"} = $resistance;
}
close(G);


print "Varieties	Green mite	White fly\n";
foreach my $name(keys(%hash))
{
	my $res_WF = "-";
	my $res_GM = "-";
	if ($hash{$name}{"White fly"}){$res_WF=$hash{$name}{"White fly"};}
	if ($hash{$name}{"Green mite"}){$res_GM=$hash{$name}{"Green mite"};}
	print "$name	".$res_GM."	".$res_WF."\n";
}
