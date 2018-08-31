#!/usr/bin/perl
use strict;
use Data::Dumper;
use Digest::SHA1 qw(sha1_hex);
use Configuration;

my $filepath = "$Configuration::HTML_DIR/accounts.txt";
my $index = 0;
my %hash;

while(!$index){
    print "Enter your id : \n";
    my $id = <STDIN>;
    chomp $id;

    print "Enter your password : \n";
    my $passw = <STDIN>;
    chomp $passw;
    #va crypter le mot de passe
    my $crypt = sha1_hex($passw);
print "$crypt \n";
    $hash{$id}=$crypt;
    
    print "Do you wants to continue adding people for total accesion of the database ? \n Print 'yes' or 'no'\n";
    my $answer = <STDIN>;
    chomp $answer;
    
    if ($answer eq 'no'){
        $index = 1;
    }
}

print Dumper (\%hash);
#ecrit id/mdp dans fichier account
if(-f $filepath){
    open (FILE, '>>', $filepath) or die "Can't open file \n";
}
else{
    open (FILE, '>', $filepath) or die "Can't open file \n";
}

foreach my $key(keys %hash){
    print FILE "$key\t$hash{$key}\n";
}
close(FILE);