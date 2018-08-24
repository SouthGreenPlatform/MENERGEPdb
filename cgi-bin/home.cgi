#!/usr/bin/perl
use strict;
use CGI;
use Time::localtime;
use Time::Local;
use File::Copy;
my $cgi = CGI->new;
use CGI::Carp 'fatalsToBrowser';
use File::Spec;
use JSON;
use Data::Dumper;
use Digest::SHA qw(sha1_hex);

use Configuration;

#####################################################
# queries
#####################################################
require "manipulateBD.pl";
Parse_Files_List();
our %hash_varietes;     
our %hash_pathogenes;
our %hash_interactions;

#########################################
# Make species and country hash
#########################################
my %hash_species;
my %hash_country;
foreach my $variety_code (sort keys(%hash_varietes))
{
	my $species_name = $hash_varietes{$variety_code}{"Species"};
	my $country_name = $hash_varietes{$variety_code}{"Country"};
	$hash_species{$species_name} = $species_name;
        $hash_country{$country_name}++;	
}
############################################
# Make country pathogen and pathogen hash
############################################
my %hash_country_patho;
my %pathogen;
foreach my $patho (sort keys(%hash_pathogenes))
{
	my $country_patho = $hash_pathogenes{$patho}{"Country"};
	my $pathotype = $hash_pathogenes{$patho}{"Pathotype/race"};
	my $type = $hash_pathogenes{$patho}{"Type"};
	$hash_country_patho{$country_patho} = $country_patho;
	$pathogen{$type} = $type;
}



############################################
#Creation of head and footer
############################################
#if pictures in directory logo_banniere, display logo in the banner
my @files;
my $URL_ban = "$Configuration::HTML_URL/logos/logo_banniere/"; 
my $rep_ban = "$Configuration::HTML_DIR/logos/logo_banniere";
opendir(REP,$rep_ban) or die "Error : $!\n"; 

while(defined(my $fic=readdir REP)){
    my $f="$fic";
    if(($fic=~/.*\.jpg/) || ($fic=~/.*\.png/) || ($fic=~/.*\.jpeg/)){
        push(@files, $f);
    }
}
closedir(REP);

my $header;
if (!@files){
	$header= qq~
	<a id="top"></a>
	
	<!--  Main page  -->
	<div id ="page">
	
	<!--  Header  -->
	<h1 style='background-color:#FBFBFB'> <br/><br/>
	<p style='text-align:center;background-color:#FBFBFB'>INTERFACE FOR HOST-PATHOGEN INTERACTIONS</p>
	<br/>
	</h1>
	~;
}
else{
	 $header = qq~
	<a id="top"></a>
	
	<!--  Main page  -->
	<div id ="page">
	
	<!--  Header  -->
	<h1 style='background-color:#FBFBFB'> <br/><br/>
	<p style='text-align:center;background-color:#FBFBFB'>INTERFACE FOR HOST-PATHOGEN INTERACTIONS <img src="$URL_ban@files" width=5%"></p>
	<br/>
	</h1>
	~;
}

my $footer = qq~
<!--  Anchor  -->
<div id="top">
<a href="#top"><u><strong><font size='3' color='#550'>Top</u></strong></font></a>
</div>

<!--  Footer  -->
<br/>
<hr/>
<p>
<div align="center">
<table>
<tr>
<td valign="center" align="center" width="1%">
<td valign="center" align="center" width="15%"><a href="http://www.ird.fr" target="_blank"><img alt="IRD logo" src="$Configuration::HTML_URL/logos/logo_ird.png" width="35%"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.umr-rpb.fr" target="_blank"><img alt="IPME logo" src="$Configuration::HTML_URL/logos/IPME_logo.png" width="35%"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://africarice.org/" target="_blank"><img alt="AfricaRice logo" src="$Configuration::HTML_URL/logos/AfricaRice_logo.jpg" width="35%"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.grisp.net/main/summary" target="_blank"><img alt="GRiSP logo" src="$Configuration::HTML_URL/logos/GRiSP_logo.jpg" width="35%"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.diade-research.fr/" target="_blank"><img alt="DIADE logo" src="$Configuration::HTML_URL/logos/DIADE_logo.png" width="35%"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.cirad.fr/" target="_blank"><img alt="CIRAD logo" src="$Configuration::HTML_URL/logos/CIAT-Logo-p.jpg" width="35%"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.cirad.fr/" target="_blank"><img alt="CIRAD logo" src="$Configuration::HTML_URL/logos/CIRAD_logo.gif" width="35%"/></a></td>
</td>
</tr>
</table>
</div>
</p>

~;

############################################
#  CGI parameters
############################################
my $action = $cgi -> param('action');
my $species = $cgi -> param('species');
my $country = $cgi -> param('country');
my $variete = $cgi -> param('variete');
my $session = $cgi -> param('session');
my $display = $cgi -> param('display');
my $var = $cgi -> param('var');
my $species2 = $cgi -> param('species2');
my $variety2 = $cgi -> param('variety2');
my $pathogen = $cgi -> param('pathogen');
my $country_pathogenes = $cgi -> param('country_pathogenes');
my $pathotype = $cgi -> param('pathotype');
my $interaction_type = $cgi -> param('interaction_type');
my $country_varieties = $cgi -> param('country_varieties');
my $ListElements = $cgi -> param('ListElements');
my $pathogene = $cgi -> param('pathogene');
my $bouclade = $cgi -> param('bouclade');
my $Pathogens = $cgi -> param('pathogens');
my $operator = $cgi -> param('operator');


my $SCRIPT_NAME = "home.cgi";

if (!$session)
{
        $session = int(rand(10000000000000));
}


=pod

=head2 displayInputForm

B<Description>      : display a submitting form

B<ArgsCount>        : 0

B<Return>           : void

B<Exception>        :

B<Example>:

=cut


###
sub Display_InputForm()
{
    print $cgi->header();
	my $stylefile = "biome.css";
	if ($cgi -> param("mode") eq "simple"){
		$stylefile = "biome_simple.css";
	}
	print $cgi->start_html(
		-title  => "PathostDB",
		-meta   => {'keywords'=>'Riz Africain, Phytopathogénes','description'=>'Database for Plant-Pathogen Interaction analysis'},
		-script => [
					{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/javascript2/jquery-1.4.4.min.js"},
					{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/javascript2/jquery-ui-1.8.9.custom.min.js"},
					{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/fonction_parcel.js"},
		
					{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/highmaps.js"},
					{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/africa.js"},
					{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/exporting.js"},
		
					{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/slides/js/jquery.jDiaporama.js"},
					{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/slides/js/script.js"},],

		-style  => [
					{'src'=>,"$Configuration::CSS_URL/style.css",'type'=>'text/css'},
					{'src'=>,"$Configuration::CSS_URL/jQuery_UI_CSS_Framework_1.8.9.css" ,'type'=>'text/css'},
					{'src'=>,"$Configuration::CSS_URL/biome.css",'type'=>'text/css'}]

	);

	print $header;
	
	###
	#Website configuration
	my $interface;
	my $search1;
	my $name_specie;
	my $name_country;
	my $name_variety;
	if ("$Configuration::CONF_INTERFACE" == 0){
		$interface = "Plants";
		$search1 = "Multipathogene Basic Search";
		$name_specie = "Species";
		$name_country = "Country of variety";
		$name_variety ="Variety";
	}
	else {
		$interface = "Parcel";
		$search1 = "Epidemiogical data";
		$name_specie = "Zone &nbsp;&nbsp;&nbsp;&nbsp;";
		$name_country = "Site of parcel &nbsp; ";
		$name_variety ="Parcel id";
	}
	###

	my $tab = qq~

	<!--  Contenu principal  -->	
	<div id='content'>
	
	<script>
	\$(function() {
	   \$( "#tabs" ).tabs();
	});
	</script>
	
	<script>
	
	function myFunction()
			{
					window.open();
			}
	</script>
	
	<!--  Tabs  -->
	<div id='tabs'>
	
	<ul id="menu">
		<li><a href='#Overview'>Overview</a></li>
		<li><a href='#Plants'>$interface</a></li>
		<li><a href='#Pathogens'>Pathogens</a></li>
		<li><a href='#Search'>$search1</a></li>
		<li><a href='#Login'>Login</a></li>
	</ul>
	
	~;
	print $tab;

	#delete temporary present for more than one day
	#system "find $Configuration::TMP_DIR -name '*.conf' -type f -mtime +1 -delete";
	system "find $Configuration::TMP_DIR -type f -mtime +1 -delete";
	system "find $Configuration::JSON_DIR -name '*.json' -type f -mtime +1 -delete";

	
	####################################################################
	# Overview
	####################################################################
	print "<div id='Overview'>";
	print "<br/>";	

	print "<div id='overview'>";
	print "<h2 style='color:rgb(51,153,102)'>Welcome ! </h2>";
	
	print "<div id='overview2'>";
	
	#About the interface
	print "<p>
	<u><strong><font size='3' color='#550'>About the project</font></strong></u>
	<br/><br/>";
	my $Conf = "$Configuration::HTML_DIR/config_home.txt";
	open (my $info , "<", $Conf) or die ("erreur: \n $!\n");
	while(my $line = <$info>){
		chomp $line;
		if ($line eq ''){
			print "<br/>";
		}
		if ($line =~/^\t/){
			print "<p style='text-indent: 5em;'> $line </p>";
		}
		print "<p> $line </p>";
	}
	print "</p>";
	print "<br/>";
	close($info);
	
	print "<br/><br/>";
	
	#Partners
	#select pictures that will appear in partners section
	my @files_partners;
	my $URL_partners = "$Configuration::HTML_URL/logos/partners/"; 
	my $rep_partners = "$Configuration::HTML_DIR/logos/partners";
	opendir(REP,$rep_partners) or die "Error : $!\n"; 
	
	while(defined(my $fic=readdir REP)){
		my $f="$fic";
		if(($fic=~/.*\.jpg/) || ($fic=~/.*\.png/) || ($fic=~/.*\.jpeg/)){
			push(@files_partners, $f);
		}
	}
	closedir(REP);
	
	print "<p>
	<u><strong><font size='3' color='#550'>Partners</font></strong></u>
	<div align=\"justify\">
	<table>
	<tr>
	<td valign=\"center\" align=\"center\" width=\"1%\">";
	for my $elem(@files_partners){
	print "<td valign=\"center\" align=\"center\" width=\"15%\"><img alt=\"$elem\" src=\"$URL_partners/$elem\" height=\"50\"/></a></td>";
	}
	print "</td>";
	print "</tr>";
	print "</table>";
	print "</div>";
	print "</p>";
	print "<br/><br/>";
	
	#About PathostDB
	print "<p>
	<u><strong><font size='3' color='#550'>About PathostDB</font></strong></u><br/>
	PathostDB is a web-based database providing access to host-pathogen interactions between plants and pathogens.</p>
	<p>A documentation including the general structure of the software, as well as instructions on how to install it and get started with it is available
	<a href ='https://mairaxb.github.io/PathostDB/' style='color:rgb(51,153,102)'> here</a>. </p>";
	print "<br/>";
	print "</div>";
	print "</div>";
	
	print "</div>";
	print "<p style='text-align:center'> Powered by <a href='https://mairaxb.github.io/PathostDB/'><img src='$Configuration::HTML_URL/logos/logo_pathostDB.png' width=5%></a></p>";
	
	####################################################################
    # Plants
    ####################################################################
    print "<div id='Plants'>";
	print "<br/><br/><br/>";

	print "<div id='Plantstab'>";
	#Generate Highmaps Google maps 
	#if longitude and latitude are present in the hash_varieties => creation of these 2 tabs
	#if these informations aren't present => creation of Highmaps tab only
	my $val_coord = 0;
	for my $key (sort keys %hash_varietes){
		if(exists($hash_varietes{$key}{'Longitude'}) or ($hash_varietes{$key}{'Latitude'})){
		$val_coord++;
		}
		else{
		$val_coord = $val_coord;
		}
	}
	
	if ($val_coord != 0){
		print "<div id='Global'>";
		print "<div id='left'>";
		print "<div id='circle'>";
		print "<iframe src='$Configuration::CGI_URL/highmaps.cgi' width='100%' height='700' style='border:solid 0px black;'></iframe>";	
		print "</div>";
		print "</div>";
		
		print "<div id='middle'></div>";
		
		print "<div id='right'>";
		print "<div id='circle'>";
		print "<iframe src='$Configuration::CGI_URL/countries_geo.cgi?session=4' width='100%' height='700' style='border:solid 0px black;'></iframe>";	
		print "</div>";
		print "</div>";
		print "</div>";
	}
	else{
		print "<div id='right'>";
		print "<div id='circle'>";
		print "<iframe src='$Configuration::CGI_URL/highmaps.cgi' width='100%' height='700' style='border:solid 0px black;'></iframe>";	
		print "</div>";
		print "</div>";
	}
	
	#Generate Highcharts
	print "<div id='circle'>";
	print "<iframe src='$Configuration::CGI_URL/chrom_viewer.cgi?session=4' width='100%' height='700' style='border:solid 0px black;'></iframe>";
	print "</div>";
	
	 print "</div>";

	
	print "</div>";
	
	####################################################################
    # Pathogens
    ####################################################################
    print "<div id='Pathogens'>";
	print "<br/><br/><br/>";
	
	print "<div id='Global'>";
	print "<div id='left'>";
	print "<div id='circle'>";
	print "<iframe src='$Configuration::CGI_URL/pathogen_geo.cgi' width='100%' height='700' style='border:solid 0px black;'></iframe>";
	print "</div>";
	print "</div>";
	
	print "<div id='middle'></div>";
	
	print "<div id='right'>";
	print "<div id='circle'>";
	print "<iframe src='$Configuration::CGI_URL/carroussel.cgi' width='100%' height='700' style='border:solid 0px black;'></iframe>";
	print "</div>";
	print "</div>";
	print "</div>";
	
	print "</div>";
	
	
	####################################################################
	# Search tab
	####################################################################
	print "<div id='Search'>";
	print "<p> Choose between Basic search tool or Advanced search tool : </p>";

	print "<form name='form_Search' form id='formid' action ='one.php' method='post'>";
	print "<input type='radio' checked  name='cardType'  id='one' class='css-checkbox' value='basic'> Basic";
	print "<input type='radio' name='cardType' id='two'  class='css-checkbox'  value='adv'> Advanced";
	
	print "<div id='a'>";
	print "<form name='form_Search' id='form_Search' method ='post' action ='home.cgi'>";
	print "<br/><br/>";
	print "<fieldset>";
	print "<legend><b>Search fields</b></legend>";
	
	##############  Table of pathogens with different phenotypes  ##############
	print "<table class='pathogens'>";
	if ($Configuration::CONF_INTERFACE == 0){
		my $list_patho = join(";",sort keys %pathogen);
		$list_patho=~s/\n//g;
		$list_patho=~s/\r//g;
		print "<input type=hidden name='PathogenNames' value=$list_patho>";
		print "<td>";	
		foreach my $pathogeneName (sort keys %pathogen)
		{
			if ($pathogeneName){
				print "<tr align=left><td align=right><b>$pathogeneName : </b>";  
				print "<input type='checkbox' name='$pathogeneName' value='R' id='$pathogeneName' />Resistant";
				print "<input type='checkbox' name='$pathogeneName' value='MR' id='$pathogeneName' />Medium Resistant";
				print "<input type='checkbox' name='$pathogeneName' value='S' id='$pathogeneName' />Susceptible&nbsp;&nbsp;";
			}
		}
		print "</td>";
	}
	if ($Configuration::CONF_INTERFACE == 1){
		my $list_patho = join(";",sort keys %hash_pathogenes);
		$list_patho=~s/\n//g;
		$list_patho=~s/\r//g;
		print "<input type=hidden name='PathogenNames' value=$list_patho>";
		print "<td>";	
		foreach my $pathogeneName (sort keys %hash_pathogenes)
		{
			if ($pathogeneName){
				print "<tr align=left><td align=right><b>$pathogeneName : </b>";  
				print "<input type='checkbox' name='$pathogeneName' value='R' id='$pathogeneName' />Absence";
				print "<input type='checkbox' name='$pathogeneName' value='S' id='$pathogeneName' />Presence&nbsp;&nbsp;";
			}
		}
		print "</td>";
	}

	print "</tr>";
	print "</table>";
	
	##############  Free search area by name of variety  ##############
	print "<br/>";
        print "<dt><strong>Input</strong></dt>";
        print "<table>";
	print "<tr>";
	print "<td valign=center>Enter a list $name_variety";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "</td>";
	print "<td>";
	print "<textarea rows='8' cols='20' name='var'>$var</textarea>";
	print "</td>";
    print "<tr>";
	print "<td>";
	print "<dt><strong>Filters</strong></dt>";
	print "</td>";
	print "</tr>";
	
	####
	#species
	print "<br/>";
	print "<table>";
	print "<tr>";
	print "<td valign=center>Enter $name_specie ";
	print "</td>";
	print "<td>";
	if ($Configuration::CONF_INTERFACE == 0){
	print "<select multiple name=species1_0 id=species1_0 size=3 onchange='update_countries(\"$Configuration::CGI_URL/display_ajax.cgi\"); update_var(\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
	foreach my $species(sort keys(%hash_species)){
		print "<option value='$species'>$species</option>\n";
        }
        print "</select>";
	}
	
	elsif ($Configuration::CONF_INTERFACE == 1){
		print "<select multiple name=species1_0 id=species1_0 size=3 onchange='update_countries(\"$Configuration::CGI_URL/display_ajax.cgi\"); update_var(\"$Configuration::CGI_URL/display_ajax.cgi\"); update_date(\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
		foreach my $species(sort keys(%hash_species)){
			print "<option value='$species'>$species</option>\n";
			}
        print "</select>";	
	}
	print "</td>";
	print "</tr>";
	print "</table>\n";
	
	#country
	print "<br/>";
	print "<table>";
	print "<tr>";
	print "<td valign=center> $name_country ";
	print "</td>";
	print "<td>";
	if ($Configuration::CONF_INTERFACE == 0){
	print "<select multiple name=country1_0 id=country1_0 size=3 onchange='updateVar2(\"$Configuration::CGI_URL/display_ajax.cgi\"); '>\n";
	}	
	if ($Configuration::CONF_INTERFACE == 1){
	print "<select multiple name=country1_0 id=country1_0 size=3 onchange='updateVar2(\"$Configuration::CGI_URL/display_ajax.cgi\"); update_date2(\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
	}
        foreach my $country (sort keys(%hash_country)){
		print "<option value='$country'>$country</option>\n";
        }
    print "</select></td></tr></table>\n";

	
	#variety
	print "<br/>";
	print "<span id='varieties_select'>";
	print "<table>";
	print "<tr>";
	print "<td valign=center>Enter $name_variety ";
	print "</td>";
	print "<td>";
	print "<select multiple name=variete id=variete1_0 size=15>\n";
        foreach my $variete(sort keys(%hash_varietes)){      
                print "<option value='$variete'>$variete</option>\n";
        }
    print "</select>";
	print "</td>";
	print "</tr>";
	print "</table>\n";
	print "</span>\n";
	
	#date
	if ($Configuration::CONF_INTERFACE == 1){
	print "<br/>";
	print "<table>";
	print "<tr>";
	print "<td valign=center> Date &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
	print "</td>";
	print "<td>";
	my $year;
	my @list_year;
	print "<select multiple name=date id=date1_0 size=3>\n";
        foreach my $var (sort keys(%hash_interactions)){
			foreach my $date (sort keys %{$hash_interactions{$var}}){
					$year = $hash_interactions{$var}{"Date"};
					if($year ~~ @list_year){next;}
					else{
					push (@list_year, $year)
					};
			}
		}
		for my $el(@list_year){
		print "<option value='$el'>$el</option>\n";
        }
    print "</select></td></tr></table>\n";
	

	}
	#result table
	print "<br/><br/>";
	print "<input type='button' class='submit' value='Search' onclick='getBasic2(\"$Configuration::CGI_URL/display_ajax.cgi\");'/>";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "<button id='refresh' type='reset' class='refresh'> Reset </button>";
    print "</fieldset>";       
	print "</form>";
	print "<br/>";	
	print "<fieldset>";
    print "<legend><b>Results display</b> </legend>";
	print "<br/><br/>";
	print "<div id='results_Search'></div>";
    print "</fieldset>";       
	print"</div>";
	
    #####################################################################
	# Advanced Search tab
	#####################################################################
	print "<div id='b'>";
    print "<form name='form_Advanced' method ='post' action ='home.cgi'>";
	print "<br/><br/>";
    print "<fieldset>";
	print "<script type='text/javascript'>var counter=0;</script>";
    print "<legend><b>Search fields</b></legend>";
	print "<br/><br/>";
	my %hash_interaction_type;
	if ($Configuration::CONF_INTERFACE == 0){
		%hash_interaction_type = ("R"=> "R", "MR"=> "MR", "S"=>"S");
	}
	if ($Configuration::CONF_INTERFACE == 1){
		%hash_interaction_type = ("R"=> "R", "S"=>"S");
	}
	##############  Headline of the table  ##############
	print "<table id='mytable' border='1' CELLSPACING='0' width='90em 10%'>";
	print "<tr>";
	#config
	if ($Configuration::CONF_INTERFACE == 0){
		print "<th colspan='3'>$interface</th>";
		print "<th colspan='3'>Pathogen</th>";
		print "<th colspan='1'>Interactions</th>";
		print "</tr>";
		print "<th>$name_specie</th>";
		print "<th>$name_country</th>";
		print "<th>$name_variety</th>";
		print "<th >Pathogen</th>  "; 
		print "<th>Country of pathogen</th>";
		print "<th>Pathotype</th> ";
		print "<th>Interactions</th>";
	}
	if ($Configuration::CONF_INTERFACE == 1){
		print "<th colspan='3'>$interface</th>";
		print "<th colspan='2'>Pathogen</th>";
		print "<th colspan='1'>Interactions</th>";
		print "</tr>";
		print "<th>$name_specie</th>";
		print "<th>$name_country</th>";
		print "<th>$name_variety</th>";
		print "<th >Disease</th>  "; 
		print "<th>Country of pathogen</th>";
		print "<th>Presence / Absence</th>";
	}
	print "<tr id='0'>";  
	
	###########################  Part Plante  ###########################
	##############  Species span  ##############
	print "<td align=center>";
	print "<select name=0 id=species2_0 onChange='getCountryVarieties(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");getVarieties1(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\")'>\n";
	print "<option value='All'>All</option>\n";
	foreach my $species(sort keys(%hash_species)){
		print "<option value='$species'>$species</option>\n";
        }
	print "</select>\n";
	print "</td>";
	
	##############  Country_varietes span  ##############
	print "<td align=center><span id='PaysdesVarietesSpan_0'>\n"; 
	print "<select name=0 id=country_varieties_0 onChange='getVarieties2(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
	print "<option value='All'>All</option>\n";
        foreach my $country(sort keys(%hash_country)){     
		my $nb_var = $hash_country{$country}; 
		if ($country){print "<option value='$country'>$country($nb_var)</option>\n";}
        }	
	print "<option></option>\n";
	print "</select></span>\n";
	print "</td>";
	
	##############  Varieties span ############## 
	print "<td align=center><span name=0 id='VarietesSpan_0'>\n"; 
	print "<select name=0 id=variety2_0>\n";
	print "<option value='All'>All</option>\n";
        foreach my $variety2(sort keys(%hash_varietes)){      
		print "<option value='$variety2'>$variety2</option>\n";
        }
	print "</select></span>\n";
	print "</td>";
	
	###########################  Part Pathogens  ###########################
	#config
	if ($Configuration::CONF_INTERFACE == 0){
		##############  Pathogens span  ##############
		print "<td align=center><span id='PathogenesSpan_0'>";
		print "<select name=0 id=pathogen_0 onChange='getCountryPathogenes(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");getPathotype1(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
		print "<option value='All'>All</option>\n";
			foreach my $pathogen(sort keys(%pathogen)){      
			if ($pathogen){print "<option value='$pathogen'>$pathogen</option>\n";}
			}
		print "</select></span>\n";
		print "</td>";
		
		##############  Country_pathogens span  ##############
		print "<td align=center><span id='CountryPathogenesSpan_0'>\n";
		print "<select name=0 id=country_pathogenes_0 onChange='getPathotype2(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
		print "<option value='All'>All</option>\n";
			foreach my $country_pathogenes(sort keys(%hash_country_patho)){      
			if ($country_pathogenes){print "<option value='$country_pathogenes'>$country_pathogenes</option>\n";}
			}
		print "</select></span>\n";
		print "</td>";
		
		##############  Pathotypes span  ##############
		print "<td align=center><span name=0 id='PathotypeSpan_0'>\n";
		print "<select name=0 id=pathotype_0>\n";
		print "<option value='All'>All</option>\n";
			foreach my $pathotype(sort keys(%hash_pathogenes)){      
			print "<option value='$pathotype'>$pathotype</option>\n";
			}
		print "</select></span>\n";
		print "</td>";
		
		##############  Interactions span  ##############
		print "<td align=center>";
		print "<select name=interaction_type_0 id=interaction_type_0>\n";
		print "<option value='All'>All</option>\n";
			foreach my $interaction_type(sort keys(%hash_interaction_type)){      
			print "<option value='$interaction_type'>$interaction_type</option>\n";
			}
		print "</select>\n";
		print "</td>";
	}
	
	if ($Configuration::CONF_INTERFACE == 1){
		##############  Pathogens span  ##############
		print "<td align=center><span id='PathogenesSpan_0'>";
		print "<select name=0 id=pathogen_0 onChange='getCountryPathogenes(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
		print "<option value='All'>All</option>\n";
			foreach my $pathogen(sort keys(%hash_pathogenes)){      
			if ($pathogen){print "<option value='$pathogen'>$pathogen</option>\n";}
			}
		print "</select></span>\n";
		print "</td>";
		
		##############  Country_pathogens span  ##############
		print "<td align=center><span id='CountryPathogenesSpan_0'>\n";
		print "<select name=country_pathogenes_0 id=country_pathogenes_0'>\n";
		print "<option value='All'>All</option>\n";
			foreach my $country_pathogenes(sort keys(%hash_country_patho)){      
			if ($country_pathogenes){print "<option value='$country_pathogenes'>$country_pathogenes</option>\n";}
			}
		print "</select></span>\n";
		print "</td>";
	#}
	##############  Interactions span  ##############
	print "<td align=center>";
	print "<select name=interaction_type_0 id=interaction_type_0>\n";
	print "<option value='All'>All</option>\n";
    foreach my $interaction_type(sort keys(%hash_interaction_type)){
		if($interaction_type eq "R"){
			print "<option value='$interaction_type'>0</option>\n";
		}
		if($interaction_type eq "S"){
			print "<option value='$interaction_type'>1</option>\n";
		}
        }
	print "</select>\n";
	print "</td>";
	}
	print "</tr>";	
	print "</table>";
	##############  End of table  ##############
	
    print "<input type='button' value='+' style='left:90%; position:absolute;' onclick='counter++;addField(counter);'/></br></br>";  
	print "<input type='button' value='-' style='left:90%; position:absolute;' onclick='counter--;removeField(counter);'/></br></br>";
	my @TabOperator = ("And", "Or");
	print "<select name=0 id=operator_0 style='left:90%; position:absolute;'>\n";
	foreach my $op (@TabOperator){
		if ($op =~ /Or/) {
			print "<option value='Or' selected>Or</option>";
		}
		else{
			print "<option value='$op'>$op</option>";
		}
		print "</br></br>";
    }	
	print "</select>\n";
	print "</br></br></br><br/><br/>";
	print "<input type='button' class='submit' value='Search' style='left:70%; position:absolute;' onclick='getAdvanced(counter,\"$Configuration::CGI_URL/display_ajax.cgi\");'/>";
	print "<button id='refresh' type='reset' class='refresh' style='left:80%; position:absolute;'>Reset</button>";
	print "</br></br>";
	print "</fieldset>";
    print "</form>";
	print "<br/>";
	
	##############  End of  form tag  ##############
        print "<fieldset>";
        print "<legend><b>Results display</b> </legend><br/><br/>";
        print "<div id='results_Advanced'></div>";
        print "</fieldset>";
	print "</div>";
	print "</form>";
	
	
	print <<"SEARCH";
	<style>
	#b{
	display:none;  
	}
	</style>
	
	<script type="text/javascript" charset="utf-8">
	\$('input[type=radio].css-checkbox').click(function(){
	  if (this.id=="one"){
		  \$('div#a').show();
		  \$('div#b').hide();

	  }
	  else {
		   \$('div#a').hide();
		  \$('div#b').show();

	  }
	});
	</script>

	
SEARCH

	
	print "</div>";
	


	#####################################################################
	# Login
	#####################################################################
	print "<div id='Login'>";
	print "<br/><br/><br/>";
    print "<form name='form_Login' method ='post' action ='login.cgi'>";
	print "<center>";
	my $session_dir = "$Configuration::HTML_DIR/tmp/";
	my $good_identifiant = 'test';
	my $good_password = 'pass';
	my $identifiant = $cgi->param('identifiant');
	my $motdepasse = $cgi->param('motdepasse');
	my $message_erreur = '';
	my $session = $cgi -> param('session');
	my $cookie = $cgi->cookie( -name => $session );
	my $file_session = File::Spec->catfile( $session_dir, 'sess_' . $cookie );
	
	#create tmp log file
	my $LOG = "$Configuration::TMP_DIR/log.info";
    open (F , ">", $LOG) or die ("erreur: \n $!\n");
	print F "no \n";
	
	
	#create log account file
	my $FILE = "$Configuration::TMP_DIR/log_account.txt";
	open (FILE , ">", $FILE) or die ("erreur: \n $!\n");
	my $crypt1 = sha1_hex("pass");
	my $crypt2 = sha1_hex("mamama");
	print FILE "test\t $crypt1";
	print FILE "\n";
	print FILE "mbarca\t $crypt2";
	print FILE "\n";
	#my $FILE = "$Configuration::HTML_DIR/log_account.txt";
	#open (L, $FILE) or die ("erreur: \n $!\n");
	#print L "test $crypt1";
	#print L "test $crypt2";
	close(F);
	close(FILE);
	
	
	print "File upload require authentication.<br/> Please enter your username and password.";
	print "<br/><br/>";
	print "<table class='center'>";
	print "<tr>";
	print "<td>User Name :</td>";
	print "<td><input name='identifiant' type='text' size='50' alt='User Name'>";
	print "</td>";
	print "</tr>";
	print "<tr>";
	print "<td>Password :</td>";
	print "<td>";
	print "<input name='motdepasse' type='password' size='50' alt='password'>";
	print "</td>";
	print "</tr>";
	print "<tr>";
	print "<td colspan='2' style='padding-top:20px;text-align:center;'>";
	print "<input name='connexion' type='submit' value='Login'>";
	print "</td>";
	print "</tr>";
	print "</table>";
	print "</form>";	
	if ( defined $message_erreur ) { print $message_erreur; }
		
	print "</center>";
        print "</div>";
        print "</div>";
	
	

	if ($cgi -> param("mode") ne "simple"){	
	        print $footer;
	}
        print $cgi->end_html;
}

Display_InputForm();
