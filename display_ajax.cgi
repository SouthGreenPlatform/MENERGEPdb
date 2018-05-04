#!/usr/bin/perl -w
use CGI;

use strict;
use warnings;
my $cgi = CGI->new();
use Data::Dumper;

use Configuration;

############################################################################
#Import script Initialisation_Enrichment_BD.pl
############################################################################
require "manipulateBD.pl";
Parse_Files_List();
our %hash_varietes;     
our %hash_pathogenes;
our %hash_interactions;

my $synonyme1;
my $synonyme2;
my $synonyme3;
my $synonyme4;
############################################################################
#Parameters sent to JavaScript functions
############################################################################
my $action = $cgi -> param('action');
my $species = $cgi -> param('species');
my $country = $cgi -> param('country');
my $variete = $cgi -> param('variete');
my $session = $cgi -> param('session');
my $display = $cgi -> param('display');
my $var = $cgi -> param('var');
my $species2 = $cgi -> param('species2');
my $variety2 = $cgi -> param('variety2');
my $counter = $cgi -> param('counter');
my $pathogen = $cgi -> param('pathogen');
my $country_pathogenes = $cgi -> param('country_pathogenes');
my $pathotype = $cgi -> param('pathotype');
my $interaction_type = $cgi -> param('interaction_type');
my $country_varieties = $cgi -> param('country_varieties');
my $ListElements = $cgi -> param('ListElements');
my $choix = $cgi -> param('choix');
my $pathogene = $cgi -> param('pathogene');
my $bouclade = $cgi -> param('bouclade');



############################################################################
#Make session for each user
############################################################################
if ($cgi -> param('session') =~/(\d+)/)
{
        $session = $1;
}
if (!$session){
        $session = int(rand(10000000000000));
}
my $execution_dir = "$Configuration::TMP_DIR";

print $cgi->header();
        print $cgi->start_html(
                -title  => "MenergepDB",
                -meta   => {'keywords'=>'TAL,xanthomonas','description'=>'TAL target finder'},
                -script => [{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/javascript/jquery-1.4.4.min.js"},{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/javascript/jquery-ui-1.8.9.custom.min.js"},{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/fonctions.js"}],

        );

############################################################################
#Query
############################################################################
my %hash_species;
my %hash_country;
foreach my $i (keys(%hash_varietes)){
	my $species_name = $hash_varietes{$i}{"Species"};
	my $country_name = $hash_varietes{$i}{"Country"};
	$hash_species{$species_name} = $species_name;
        $hash_country{$country_name} = $country_name;
}
my %hash_country_patho;
my %pathogen;
foreach my $j (sort keys(%hash_pathogenes))
{
	my $country_patho = $hash_pathogenes{$j}{"Country"};
	my $pathotype = $hash_pathogenes{$j}{"Pathotype/race"};
	my $type = $hash_pathogenes{$j}{"Type"};
	$hash_country_patho{$j} = $country_patho;
	$pathogen{$type} = $type;
}
my %interAct;
foreach my $i (sort keys(%hash_pathogenes))
{
	my $type = $hash_pathogenes{$i}{"Type"};
	foreach my $j (sort keys (%hash_interactions)){
		my $ref_hashhh = $hash_interactions{$j};
                my %ref_hashhh2 = %$ref_hashhh;
                foreach my $k (keys %ref_hashhh2){
			my $p = $hash_interactions{$j}{$k};
			if ($i =~ $k) {
				$interAct{$j}{$type}{$k} = $p;
			}
		}	
	}
}
my @TabPath;
foreach my $i (sort keys(%pathogen))
{
	push @TabPath, $i;
}
#print "@TabPath";
#print Dumper (\%interAct);
#print Dumper (\%hash_varietes);
#
#exit;
my $compteur = 0;

my $val_log;
my $LOG = "$Configuration::TMP_DIR/log.info";
open (F , "<", $LOG) or die ("erreur: \n $!\n");
while(<F>){
	chomp;
	$val_log = $_;
}
close(F);

#
##Menu deroulant automatique pour onglet Basic search
#
#upload country field base on specie name entered
if ($action eq "changeCountryBasic") {
	print "<select name=$counter id=country1_0".$counter." onChange='getVar2(this.name);'>\n";
	#print "<select name=0 id=country_varieties_0 onChange='getVarieties2(this.name,VarietesSpan_);'>\n";
	#print "<option value='All'>All</option>\n";
	if($ListElements!~/All/){
		my %hashC;
		foreach my $i (sort keys(%hash_varietes)){
			my $speciesname = $hash_varietes{$i}{"Species"};
			my $countryname = $hash_varietes{$i}{"Country"};
			if ($speciesname =~ m/\b$ListElements\b/){
				$hashC{$countryname}++;
			}
		}
		foreach my $country (sort keys (%hashC )){
			my $nboccurence = $hashC{$country};
			print "<option value='$country'>$country($nboccurence)</option>\n";
		}
	}
	elsif($ListElements=~/All/) {
		foreach my $i(sort keys(%hash_country))
		{
			print "<option value='$i'>$i</option>\n";
		}
	}
	print "</select>\n";
	exit;
}

#upload variety field base on specie name entered
if ($action eq "changeVarBasic") {
	my @tabElements = split(/,/,$ListElements);
	my $firstelement = $tabElements[0];
	my $secondelement = $tabElements[1];
	print "<select name=$counter id=variety1_".$counter." >\n";
	#print "<option value='All'>All</option>\n";
	if ($firstelement!~/All/) {
		my %hashV;
		foreach my $variete(sort keys(%hash_varietes)){
			my $speciesname = $hash_varietes{$variete}{"Species"};
			if (($firstelement =~/$speciesname/)) {
				$hashV{$variete}++;
			}		
		}
		foreach my $variety (sort keys (%hashV)){
			#my $nboccurence = $hashV{$variety};
			print "<option value='$variety'>$variety</option>\n";
		}
	}
	elsif ($ListElements=~/All/) {
		foreach my $i(sort keys(%hash_varietes)){      
		        print "<option value='$i'>$i</option>\n";
		}
	}
	print "</select>\n";
	exit;
}

#upload variety field base on country entered
if ($action eq "changeVar2Basic") {
	print "<select name=$counter id=variety1_".$counter." >\n";
	#print "<option value='All'>All</option>\n";
	my %hashV;
	if ($ListElements!~/All/) {
		if ($ListElements=~/^,/) {
			my @tabElements = split(/,/,$ListElements);
			my $element = $tabElements[1];
			foreach my $variete(sort keys(%hash_varietes)){
				my $countryname = $hash_varietes{$variete}{"Country"};
				if ($element =~ /$countryname/) {
					$hashV{$variete}++;
				}		
			}
			#print "<option value='$secondelement'>$secondelement</option>\n";
		}
		elsif($ListElements!~/^,/){
			my @tabElements = split(/,/,$ListElements);
			my $firstelement = $tabElements[0];
			my $secondelement = $tabElements[1];
			foreach my $variete(sort keys(%hash_varietes)){
				my $speciesname = $hash_varietes{$variete}{"Species"};
				my $countryname = $hash_varietes{$variete}{"Country"};
				if ($firstelement =~/$speciesname/ && $secondelement =~ /$countryname/) {
					$hashV{$variete}++;
				}		
			}
		}
		foreach my $variety (sort keys (%hashV)){
			#my $nboccurence = $hashV{$variety};
			print "<option value='$variety'>$variety</option>\n";
		}
	}
	elsif ($ListElements=~/All/) {
		foreach my $i(sort keys(%hash_varietes)){      
		        print "<option value='$i'>$i</option>\n";
		}
	}
	
	print "</select>\n";
	exit;
}
############################################################################
#Menu deroulant automatique liee pour les country varities
############################################################################
if ($action eq "changeCountry") {
	print "<select name=$counter id=country_varieties_".$counter." onChange='getVarieties2(this.name);'>\n";
	print "<option value='All'>All</option>\n";
	if($ListElements!~/All/){
		my %hashC;
		foreach my $i (sort keys(%hash_varietes)){
			my $speciesname = $hash_varietes{$i}{"Species"};
			my $countryname = $hash_varietes{$i}{"Country"};
			if ($speciesname =~ m/\b$ListElements\b/){
				$hashC{$countryname}++;
			}
		}
		foreach my $country (sort keys (%hashC )){
			my $nboccurence = $hashC{$country};
			print "<option value='$country'>$country($nboccurence)</option>\n";
		}
	}
	elsif($ListElements=~/All/) {
		foreach my $i(sort keys(%hash_country))
		{
			print "<option value='$i'>$i</option>\n";
		}
	}
	print "</select>\n";
	exit;
}
###############################################################################
#Menu deroulant automatique liee pour obtenir les varities a partir de l'espece 
###############################################################################
if ($action eq "changeVarieties1") {
	my @tabElements = split(/,/,$ListElements);
	my $firstelement = $tabElements[0];
	my $secondelement = $tabElements[1];
	print "<select name=$counter id=variety2_".$counter." >\n";
	print "<option value='All'>All</option>\n";
	if ($firstelement!~/All/) {
		my %hashV;
		foreach my $variete(sort keys(%hash_varietes)){
			my $speciesname = $hash_varietes{$variete}{"Species"};
			if (($firstelement =~/$speciesname/)) {
				$hashV{$variete}++;
			}		
		}
		foreach my $variety (sort keys (%hashV)){
			#my $nboccurence = $hashV{$variety};
			print "<option value='$variety'>$variety</option>\n";
		}
	}
	elsif ($ListElements=~/All/) {
		foreach my $i(sort keys(%hash_varietes)){      
		        print "<option value='$i'>$i</option>\n";
		}
	}
	print "</select>\n";
	exit;
}
############################################################################
#Menu deroulant automatique liee pour les varities a partir du country
############################################################################
if ($action eq "changeVarieties2") {
	print "<select name=$counter id=variety2_".$counter." >\n";
	print "<option value='All'>All</option>\n";
	my %hashV;
	if ($ListElements!~/All/) {
		my @tabElements = split(/,/,$ListElements);
		my $firstelement = $tabElements[0];
		my $secondelement = $tabElements[1];
		foreach my $variete(sort keys(%hash_varietes)){
			my $speciesname = $hash_varietes{$variete}{"Species"};
			my $countryname = $hash_varietes{$variete}{"Country"};
			if ($firstelement =~/$speciesname/ && $secondelement =~ /$countryname/) {
				$hashV{$variete}++;
			}		
		}
		foreach my $variety (sort keys (%hashV)){
			#my $nboccurence = $hashV{$variety};
			print "<option value='$variety'>$variety</option>\n";
		}
	}
	elsif ($ListElements=~/All/) {
		foreach my $i(sort keys(%hash_varietes)){      
		        print "<option value='$i'>$i</option>\n";
		}
	}
	print "</select>\n";
	exit;
}

############################################################################
#Menu deroulant automatique liee pour les pathogenes
#############################################################################
if ($action eq "changeCountryPathogenes") {
	print "<select name=$counter id=country_pathogenes_".$counter." onChange='getPathotype2(this.name);'>\n";
	print "<option value='All'>All</option>\n";
	my %hashCP;
	if ($ListElements!~/All/) {
		my @tabElements = split(/,/,$ListElements);
		my $firstelement = $tabElements[0];
		my $secondelement = $tabElements[1];
		foreach my $i (sort keys (%hash_pathogenes)){
			my $country = $hash_pathogenes{$i}{"Country"};
			my $type = $hash_pathogenes{$i}{"Type"};
			if ($type =~ m/^$firstelement$/ ) {
				$hashCP{$country}++
			}
		}
		foreach my $country_pathogenes (sort keys (%hashCP)){
			#my $nboccurence = $hashCP{$country_pathogenes};
			print "<option value='$country_pathogenes'>$country_pathogenes</option>\n";
		}		
		
	}
	if ($ListElements=~/All/) {
		foreach my $i (sort keys(%hash_pathogenes)){
			my $country = $hash_pathogenes{$i}{"Country"};
			$hashCP{$country}++
		}
		foreach my $country_pathogenes (sort keys (%hashCP)){
			print "<option value='$country_pathogenes'>$country_pathogenes</option>\n";
		}
	}	
	print "</select>\n";
	exit;
}
if ($action eq "changePathotype1") {
	print "<select name=$counter id=pathotype_".$counter.">\n";
	print "<option value='All'>All</option>\n";
	my %hashP;
	if ($ListElements!~/All/) {
		my @tabElements = split(/,/,$ListElements);
		my $firstelement = $tabElements[0];
		foreach my $i (sort keys (%hash_pathogenes)){
			my $type = $hash_pathogenes{$i}{"Type"};
			if ($type =~ m/^$firstelement$/) {
				$hashP{$i}++;
			}
		}
		foreach my $j (sort keys (%hashP)){
			print "<option value='$j'>$j</option>\n";
		}		
		
	}
	if ($ListElements=~/All/) {
		foreach my $i (sort keys(%hash_pathogenes)){
			print "<option value='$i'>$i</option>\n";
		}
	}	
	print "</select>\n";
	exit;
}

if ($action eq "changePathotype2") {
	print "$counter<select name=$counter id=pathotype_".$counter.">\n";
	print "<option value='All'>All</option>\n";
	my %hashP;
	if ($ListElements!~/All/) {
		my @tabElements = split(/,/,$ListElements);
		my $firstelement = $tabElements[0];
		my $secondelement = $tabElements[1];
		foreach my $i (sort keys (%hash_pathogenes)){
			my $type = $hash_pathogenes{$i}{"Type"};
			my $country = $hash_pathogenes{$i}{"Country"};
			if ($type =~ m/^$firstelement$/ && $country =~ m/^$secondelement$/) {
				$hashP{$i}++;
			}
		}
		foreach my $j (sort keys (%hashP)){
			print "<option value='$j'>$j</option>\n";
		}		
		
	}
	if ($ListElements=~/All/) {
		foreach my $i (sort keys(%hash_pathogenes)){
			print "<option value='$i'>$i</option>\n";
		}
	}	
	print "</select>\n";
	exit;
}

############################################################################
#Affichage des requettes de longlet Search
############################################################################
if ($action eq "getBasic2"){
	my $species_concatenation;
	my $country_concatenation;
	my $variety_concatenation;
	my $var_concatenation;
	if ($species){
		$species_concatenation = ",".$species.",";
	}
	if ($country){
                $country_concatenation = ",".$country.",";
        }
	if ($variete){
                $variety_concatenation = ",".$variete.",";
        }
	my %expected_resistance;
	my $list_patho = join(";",sort keys %pathogen);
	$list_patho=~s/\n//g;
	$list_patho=~s/\r//g;
	my $resistance_is_checked = 0;
	my $count_info_resistance = 0;
	my @patho_displayed;
	foreach my $pathogeneName (sort keys %pathogen)
	{
		my $resistance_exp = $cgi -> param('resistance_'.$pathogeneName);
		if ($resistance_exp) {
			$resistance_is_checked = 1;
			$expected_resistance{$pathogeneName}=$resistance_exp;
			$count_info_resistance++;
			push(@patho_displayed,$pathogeneName);
		}
	}
        if ($var){
                $var_concatenation = ",".$var.",";
        }

	my $OUT = "$execution_dir/table.$session.csv";
        open (F , ">$OUT");
        print F "Varietes	Species	Country	Origin	". join("\t",@patho_displayed)."\n";
	if ($species_concatenation or $country_concatenation or $variety_concatenation or $var_concatenation or $resistance_is_checked)
	{
		foreach my $variety_code (sort keys %hash_varietes)
		{
			$variety_code =~s/\r//g;
			$variety_code =~s/\n//g;
			my $species_code = $hash_varietes{$variety_code}{"Species"};
			my $country_code = $hash_varietes{$variety_code}{"Country"};
			my $origin_code = $hash_varietes{$variety_code}{"Origins"};
			my $listSyn;
			
			if ($variety_code && $variety_concatenation &&  $variety_concatenation !~ /$variety_code/) #or ($RYMV_concatenation !~ m/\b$RYMV_code\b/ && $choix =~ /and/)
			{
				next;
			}
			if ($species_code &&  $species_concatenation &&  $species_concatenation !~ /$species_code/)
			{
				next;
			}
			if ($country_code && $country_concatenation &&   $country_concatenation !~ m/\b$country_code\b/)
			{
				next;
			}
			if ($variety_code && $var_concatenation &&  $var_concatenation !~ m/$variety_code/i)
			{
				next;
			}
			my %nb_matches;
			my %infos_patho_concat;
            my %hash_alert;
			my $code;
			#my $line_var = "<a href=javascript:afficheSynonymes_varietes('$listSyn')>$variety_code</a>	$species_code	$country_code	$origin_code";
			foreach my $synonymes (keys %{$hash_varietes{$variety_code}{"Synonymes"}})
			{
				if ($synonymes !~/^.[a-zA-Z].+\d?$/)
				{
					$listSyn = "none";
				}
				if ($synonymes =~/^.[a-zA-Z].+\d?$/)
				{
					$listSyn = "$synonymes";
				}
				foreach my $i (sort keys(%interAct))
				{
					if ($variety_code =~ m/\b$i\b/)
					{
						#my $code;
						foreach my $t (keys %{$interAct{$i}})
						{
							my $concatenation='';
							foreach my $p (values %{$interAct{$i}{$t}})
							{
								$concatenation .= ','.$p;
								if ($interAct{$i}{$t}{$p}){
								
								$concatenation .= ','.$p. join( "*", @{ $interAct{$i}{$t}{$p} } );
								}
							}
							if ($concatenation =~ m/\bR\b/)
							{
								$code = "R";
							}
							elsif ($concatenation =~ m/\bMR\b/)
							{
								$code = "MR";
							}
							elsif ($concatenation =~ m/\bS\b/)
							{
								$code = "S";
							}
							else
							{
								$code = "-";
							}
							my $expected_value = $expected_resistance{$t};
							if (!$expected_resistance{$t}) {
								next;
							}
							if ($code &&  $expected_value  &&  $expected_value !~ m/\b$code\b/)
							{
								next;
							}
							
							#delete special characters
							$concatenation =~ s/-//;
							$concatenation =~ s/^,.//;
							#alert javascript
							if($concatenation=~ /\w.+/){
								$infos_patho_concat{$t} = "<a href=javascript:afficheIsolat_rymv('$concatenation','$variety_code')>$code</a>";
							}
							else {
								$concatenation = "none";
								$infos_patho_concat{$t} = "<a href=javascript:afficheIsolat_rymv('$concatenation','$variety_code')>$code</a>";
							}
							#$infos_patho_concat{$t} = "<a href=javascript:afficheIsolat_rymv('$concatenation','$variety_code')>$code</a>";
							$nb_matches{$variety_code}++;
                            
                            #alert the user if replicates are different
                            my @info_alert;
                            @info_alert = split(",", $concatenation);
							my @clear_list;
							for my $el (@info_alert){
								if ($el ne "-"){
									push(@clear_list, $el);
								}
								else{
									next;
								}
							}
							my $size = scalar @clear_list;
                            for (my $i = 0; $i<$size-1; $i++){
								if($clear_list[$i] ne $clear_list[$i+1]){
									$hash_alert{$t}=1;
								}
							}
							
						}
					} 
				}
			}
	#		print $variety_code . " " . $nb_matches{$variety_code}." " .$count_info_resistance."<br/>";
			my $line_var = "<a href=javascript:afficheSynonymes_varietes('$listSyn')>$variety_code</a>	$species_code	$country_code	$origin_code	";
			#print Dumper %hash_alert;
			if ($nb_matches{$variety_code} == $count_info_resistance) {
				$compteur++;
				print F $line_var;
				foreach my $p(@patho_displayed){
					print F  $infos_patho_concat{$p};
                    
                    if($hash_alert{$p}!=0){
                        print F "   (!)";
                    }
				}
				print F "\n";
			}
		}
	}
        close(F);
	
print "<table class='counter'><tr><td><b>$compteur entries found</b></td></tr></table>";
print "<table class='terms'><tr><td><font>Terms of resistance/susceptibility :</br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
- If a variety is found to be resistant (R) for at least one isolate or pathotype it is considered resistant (R).</br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
- Otherwise, if a variety is found to be resistant medium (MR) for at least one isolate or pathotype it is considered resistant medium (MR). </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
- Otherwise, the variety is considered suceptible(S).</br></br>
The sign (!) is used when different replicates gave different results. These results are visible by a click on the term.
</font></td></tr></table><br/><br/>";
#print Dumper $level_user;
}

############################################################################
#Affichage des requettes de l'onglet Advanced
############################################################################
if ($action eq "getAdvanced"){
	my $OUT = "$execution_dir/table.$session.csv"; #results will be written there
	open (F , ">$OUT");
	print F "Species	Country	Varieties	Pathogen	Country of pathogen	Pathotype	Interactions type	Complementary informations\n";
	my %nb_matches;
	for (my $i =1; $i <= $counter; $i++)
	{
		my $line_var;
		my $species2_concatenation;
		my $country_varieties_concatenation;
		my $variety2_concatenation;
		my $pathogen_concatenation;
		my $country_pathogenes_concatenation;
		my $pathotype_concatenation;
		my $interaction_type_concatenation;

		my $c = $i-1;		
		$species2 = $cgi -> param('species2_'.$c);
		$variety2 = $cgi -> param('variety2_'.$c);
		$pathogen = $cgi -> param('pathogen_'.$c);
		$interaction_type = $cgi -> param('interaction_type_'.$c);
		$country_varieties = $cgi -> param('country_varieties_'.$c);
		$country_pathogenes = $cgi -> param('country_pathogenes_'.$c);
		$pathotype = $cgi -> param('pathotype_'.$c);
		
		#print "$country_pathogenes $country_varieties ptho: $pathogen int: $interaction_type type: $pathotype var: $variety2 hnvh<br>";
		
		if ($species2){
			$species2_concatenation = ",".$species2.",";
		}
		if ($variety2){
			$variety2_concatenation = ",".$variety2.",";
		}
		if ($country_varieties){
			$country_varieties_concatenation = ",".$country_varieties.",";
		}
		if ($pathogen){
			$pathogen_concatenation = ",".$pathogen.",";
		}
		if ($country_pathogenes){
			$country_pathogenes_concatenation = ",".$country_pathogenes.",";
		}
		if ($pathotype){
			$pathotype_concatenation = ",".$pathotype.",";
		}	
		if ($interaction_type){
			$interaction_type_concatenation = ",".$interaction_type.",";
		}
		if ($species2_concatenation or $variety2_concatenation or $country_varieties_concatenation or $pathogen_concatenation or $pathotype_concatenation or $country_pathogenes_concatenation or $interaction_type_concatenation)
		{
			foreach my $variety2_code (sort keys (%hash_varietes))
			{
				my $species2_code = $hash_varietes{$variety2_code}{"Species"};
				my $country_varieties_code = $hash_varietes{$variety2_code}{"Country"};
				foreach my $varietes_hashInteractions (sort keys(%hash_interactions))
				{
					#check if the variety code of the specie is in the interaction file
					if ($variety2_code =~ m/\b$varietes_hashInteractions\b/)
					{			
						#value of isolat is R, MR or S
						#if status eq private
						foreach my $isolat (keys %{$hash_interactions{$varietes_hashInteractions}})
						{
							foreach my $isolatHashpatho (keys (%hash_pathogenes))
							{
								#check if isolat is in both interaction file and pathogen file
								if ($isolat =~ m/\b$isolatHashpatho\b/)
								{
									$pathogen = $hash_pathogenes{$isolatHashpatho}{"Type"};
									$country_pathogenes = $hash_pathogenes{$isolatHashpatho}{"Country"};
									$pathotype = $isolat;
									$interaction_type = $hash_interactions{$varietes_hashInteractions}{$isolat};
									$info = $hash_interactions{$varietes_hashInteractions}{"Informations"};
									
									if ( $variety2_code && $variety2_concatenation &&  ($variety2_concatenation !~ $variety2_code && $variety2_concatenation !~ /All/))
									{
										next;
									}
									if ( $species2_code &&  $species2_concatenation &&  ($species2_concatenation !~ /$species2_code/ && $species2_concatenation !~ /All/))
									{
										next;
									}
									if ( $country_varieties_code && $country_varieties_concatenation &&  ($country_varieties_concatenation !~ /$country_varieties_code/ &&  $country_varieties_concatenation !~ /All/))
									{
										next;
									}
									if ($pathotype && $pathotype_concatenation && ($pathotype_concatenation !~ m/\b$pathotype\b/ && $pathotype_concatenation !~ /All/)) {
										next;
									}
									if ($pathogen && $pathogen_concatenation && ($pathogen_concatenation !~ m/\b$pathogen\b/ && $pathogen_concatenation !~ /All/)) {
										next;
									}
									if ($country_pathogenes && $country_pathogenes_concatenation && ($country_pathogenes_concatenation !~ m/\b$country_pathogenes\b/ && $country_pathogenes_concatenation !~ /All/)) {
										next;
									}
									if ($interaction_type && $interaction_type_concatenation && ($interaction_type_concatenation !~ m/\b$interaction_type\b/ && $interaction_type_concatenation !~ /All/))
									{
										next;
									}
									
									#private data only availabe when user log in 
									if($val_log =~ /no/ && $hash_interactions{$varietes_hashInteractions}{"Status"} eq "Privee"){
										next;
									}
									
									
		
									#print $variety2_code."<br/>";
									$nb_matches{$variety2_code}++;
									#$line_var = "$species2_code	$country_varieties_code	$variety2_code	$pathogen	$country_pathogenes	$pathotype	$interaction_type \n";
									print F "$species2_code	$country_varieties_code	$variety2_code	$pathogen	$country_pathogenes	$pathotype	$interaction_type	$info	\n";
									$compteur++;
								}
							}
						}
					}
				}
			}
		}
		#print "<br/><br/>";
	}
        close(F);
	print "<table class='counter'><tr><td><b>$compteur entries found</b></td></tr></table><br/><br/><br/>";
	#print Dumper $session;
	#print Dumper $val_log;
}
############################################################################
#Make .config files
############################################################################
my $config_table .= qq~
'table'=>
{
        "select_title" => "Results table",
        "file" => "$execution_dir/table.$session.csv",
},~;
my $out = "$execution_dir/tables.$session.conf";
open(my $T, ">", "$out") or print "Couldn't open: $out";
print $T $config_table;
close($T);

############################################################################
#Display query
############################################################################
print "<iframe src='$Configuration::CGI_URL/table_viewer.cgi?session=$session' width='100%' height='800px' style='border:solid 0px black;'></iframe><br/><br/>";


