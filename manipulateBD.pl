#!/usr/bin/perl
use strict;
use warnings;
use JSON;
use Data::Dumper;
use Configuration;
#my $directory = $ARGV[0];
our %hash_varietes;     
our %hash_pathogenes;
our %hash_interactions;
my $Varieties_HashFile = "FichierVarieties2.hash";
my $Pathogenes_HashFile = "FichierPathogenes2.hash";
my $Interactions_HashFile = "FichierInteractions2.hash";

my $Varieties_JsonFile = "FichierVarieties2.json";
my $Pathogenes_JsonFile = "FichierPathogenes2.json";
my $Interactions_JsonFile = "FichierInteractions2.json";


###############################################
# Get existing JSON files into hash
###############################################
if (-e $Varieties_JsonFile) {
	open(J1,$Varieties_JsonFile);
	my $json_varietes = "";
	while (<J1>) {
		$json_varietes .= $_;
	}
	close(J1);
	my $json_varietes_decode = decode_json ( $json_varietes );
	%hash_varietes = %$json_varietes_decode;
}
if (-e $Pathogenes_JsonFile) {
	open(J2,$Pathogenes_JsonFile);
	my $json_pathogenes = "";
	while (<J2>) {
		$json_pathogenes .= $_;
	}
	close(J2);
	my $json_pathogenes_decode = decode_json ( $json_pathogenes );
	%hash_pathogenes = %$json_pathogenes_decode;
}
if (-e $Interactions_JsonFile) {
	open(J3,$Interactions_JsonFile);
	my $json_interactions = "";
	while (<J3>) {
		$json_interactions .= $_;
	}
	close(J3);
	my $json_interactions_decode = decode_json ( $json_interactions );
	%hash_interactions = %$json_interactions_decode;
}
###########################################################################
# Get_Files_List function returns a table of contents file in a directory
###########################################################################
sub Get_Files_List
{
        my $Path = $_[0];
        my $FileFound;
        my @FilesList=();

        opendir (my $FhRep, $Path)
                or die "Impossible d'ouvrir le repertoire $Path\n";
        my @Contenu = grep { !/^\.\.?$/ } readdir($FhRep);
        closedir ($FhRep);

        foreach my $FileFound (@Contenu) {
                if ( -f "$Path/$FileFound") {
                        push ( @FilesList, "$Path/$FileFound" );
                }
                elsif ( -d "$Path/$FileFound") {
                        push (@FilesList, Get_Files_List("$Path/$FileFound") );
                }
        }
        return @FilesList;
}

###########################################################################
# Parse_Files_List parse the received files to create JSON files
###########################################################################
sub Parse_Files_List()
	{
	my @Files = Get_Files_List ($Configuration::DATABASE_LOCATION) ;  #Get_Files_List ($directory);
	foreach my $File  (@Files) 
	{
		if ($File =~/git/){next;}
		open (FILE, $File)
		    or die "Could not open the file $!";
		my $first_Line = 0;
		my @Tab_header;
		my @TabSyn;
		my @Fields;
		my $i;
		my @Infos_line;		
		while (my $line = <FILE>)
		{
			chomp $line;
			$line =~s/\n//g;
			$line =~s/\r//g;
			#################################################
			# Get header for each file
			#################################################
			if ($first_Line == 0)
			{
				@Tab_header = split/\t/, $line;
				$first_Line = 1;
				next;
			}
			#######################################
			# Make varieties hash
			#######################################
			if ($Tab_header[0] =~ /Varieties/ and $Tab_header[1] =~ /Species/)
			{
				my $first_column;
				my $column_name;
				@Infos_line = split /\t/, $line;
				$first_column = $Infos_line[0];
				my $j = 1;
				foreach ($i = 1; $i <=$#Tab_header; $i++) 
				{
					$column_name = $Tab_header[$i];  
					if ($j != 3)
					{
						$hash_varietes{$first_column}{$column_name} = $Infos_line[$i];
					}
					if ($j == 3) {
						{
							$hash_varietes{$first_column}{"Synonymes"}{$Infos_line[3]} = $first_column;
						}
					}
					$j++;
				}
			}
			#######################################
			# Make pathogenes hash
			#######################################
			if ($Tab_header[0] !~ /Varieties/)
			{
				my $first_column_ref;
				my $column_name;
				@Infos_line = split /\t/, $line;
				$first_column_ref = $Infos_line[0];
				my $j = 1;
				foreach ($i = 1; $i <=$#Tab_header; $i++) 
				{
				    $column_name = $Tab_header[$i]; 
				    $hash_pathogenes{$first_column_ref}{$column_name} = $Infos_line[$i];
				    $j++;	
				}			
			}
			#######################################
			# Make interactions hash
			#######################################
			if ($Tab_header[0] =~ /Varieties/ and $Tab_header[1] !~ /Species/)
			{
				my $first_column_ref;
				my $column_name;
				@Infos_line = split /\t/, $line;
				$first_column_ref = $Infos_line[0];
				my $j = 1;
				foreach ($i = 1; $i <=$#Tab_header; $i++) 
				{
				    my $column_name = $Tab_header[$i]; 
				    $hash_interactions{$first_column_ref}{$column_name} = $Infos_line[$i];
				    $j++;               
				}
			}            
		}
	}
	
	#######################################
	# Encoding hash in JSON structure
	#######################################
	my $json_varietes = encode_json (\%hash_varietes);
	my $json_pathogenes = encode_json (\%hash_pathogenes);
	my $json_interactions = encode_json (\%hash_interactions);
	######################################################################
	# Make JSON file corresponding to each hash table
	######################################################################
	open(VARIETIES_FILE, ">$Varieties_JsonFile");
	print VARIETIES_FILE $json_varietes;
	close(VARIETIES_FILE);
	
	open(PATHOGENES_FILE, ">$Pathogenes_JsonFile");
	print PATHOGENES_FILE $json_pathogenes;
	close(PATHOGENES_FILE);
	
	open(INTERACTIONS_FILE, ">$Interactions_JsonFile");
	print INTERACTIONS_FILE $json_interactions;
	close(INTERACTIONS_FILE);
	
	
	######################################################################
	# Make HASH file corresponding to each hash table
	######################################################################
	open(VARIETIES2, ">$Varieties_HashFile");
	print VARIETIES2 Dumper (\%hash_varietes);;
	close(VARIETIES2);
	
	open(PATHOGENES2, ">$Pathogenes_HashFile");
	print PATHOGENES2 Dumper (\%hash_pathogenes);;
	close(PATHOGENES2);
	
	open(INTERACTIONS2, ">$Interactions_HashFile");
	print INTERACTIONS2 Dumper (\%hash_interactions);;
	close(INTERACTIONS2);
		
	#Hash to exporte
	#print Dumper (\%hash_varietes);
	#print Dumper (\%hash_pathogenes);
	#print Dumper (\%hash_interactions);
	
	close (FILE);    
}
	
Parse_Files_List();
#print scalar keys(%hash_interactions);
