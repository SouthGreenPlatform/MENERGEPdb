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

my $header = qq~

<link rel="icon" type="image/png" href="./Logo1.png" />
<a id="top"></a>

<!--  Main page  -->
<div id ="page">

<!--  Header  -->
<h1><img src="$Configuration::HTML_URL/logos/LogoMenergepDB.png" width=100% height=100% ></h1>

~;

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
<td valign="center" align="center" width="15%"><a href="http://www.ird.fr" target="_blank"><img alt="IRD logo" src="$Configuration::HTML_URL/logos/IRD_logo.gif" height="50"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.umr-rpb.fr" target="_blank"><img alt="IPME logo" src="$Configuration::HTML_URL/logos/IPME_logo.png"height="60"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://africarice.org/" target="_blank"><img alt="AfricaRice logo" src="$Configuration::HTML_URL/logos/AfricaRice_logo.jpg" height="60"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.grisp.net/main/summary" target="_blank"><img alt="GRiSP logo" src="$Configuration::HTML_URL/logos/GRiSP_logo.jpg" height="70"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.diade-research.fr/" target="_blank"><img alt="DIADE logo" src="$Configuration::HTML_URL/logos/DIADE_logo.png" height="65"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.cirad.fr/" target="_blank"><img alt="CIRAD logo" src="$Configuration::HTML_URL/logos/CIAT-Logo-p.jpg" height="70"/></a></td>
<td valign="center" align="center" width="15%"><a href="http://www.cirad.fr/" target="_blank"><img alt="CIRAD logo" src="$Configuration::HTML_URL/logos/CIRAD_logo.gif" height="70"/></a></td>
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
				{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/fonctions.js"},
				
                                {'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/highmaps.js"},
				{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/africa.js"},
                              	{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/exporting.js"},
				
				{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/slides/js/jquery.jDiaporama.js"},
				{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/slides/js/script.js"},		
		],

               -style  => [
				#{'src'=>,"$Configuration::HTML_URL/slides/googleapis",'type'=>'text/css'},		
				#{'src'=>,"$Configuration::HTML_URL/slides/page.css",'type'=>'text/css'},
				#{'src'=>,"$Configuration::HTML_URL/slides/style.css",'type'=>'text/css'},
				{'src'=>,"http://bioinfo-test.ird.fr:84/cgi-bin/css/style.css",'type'=>'text/css'},
				{'src'=>,"http://bioinfo-test.ird.fr:84/cgi-bin/css/jQuery_UI_CSS_Framework_1.8.9.css" ,'type'=>'text/css'},
				{'src'=>,"http://bioinfo-test.ird.fr:84/cgi-bin/css/biome.css",'type'=>'text/css'}]

        );

        print $header;

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
	<li><a href='#Plants'>Plants</a></li>
        <li><a href='#Pathogens'>Pathogens</a></li>
   	<li><a href='#Search'>Multipathogene Basic Search</a></li>
        <li><a href='#Advanced'>Multipathogene Advanced search</a></li>
        <li><a href='#Login'>Login</a></li>
</ul>

~;
        print $tab;



        ####################################################################
        # Overview
        ####################################################################
        print "<div id='Overview'>";
	print "<br/><br/><br/>";	

	print "<div id='overview'>";
	print "<h2>Welcome to MENERGEPdb !</h2>";
	
	print "<div id='overview2'>";
	print "<p>
	<u><strong><font size='3' color='#550'>MENERGEPdb</font></strong></u> is a web-based database providing access to resistance data to pathogens African rice.
	This database facilitates querying and visualization of the results of the project <a href='http://www.madagascar.ird.fr/les-activites/la-recherche3/madagascar/riz-et-pathogenes/menergep' target=_blank><font size='3' color='#550'><strong>MENERGEP</strong></font></a> but also downloading some research data.<br/>";
	print "</p>";
	print "<br/><br/>";
	
	
	#print "<div id=\"Global\">";
	#print "<div id='left'>";
	#print "<div id='circle'>";
	#print "<iframe src='http://bioinfo-test.ird.fr:84/cgi-bin/highmaps.cgi' width='100%' height='700' style='border:solid 0px black;'></iframe>";	
	#print "</div>";
	#print "</div>";
	#
	#print "<div id=\"middle\"></div>";
	#
	#print "<div id='right'>";
	#print "<div id='circle'>";
	#print "<iframe src='http://bioinfo-test.ird.fr:84/cgi-bin/chrom_viewer.cgi?session=4' width='100%' height='700' style='border:solid 0px black;'></iframe>";
	#print "</div>";
	#print "</div>";
	#print "</div>";
	

	#print "<div id=\"Global\">";
	#print "<div id='left'>";
	#print "<div id='circle'>";
	#print "<iframe src='http://bioinfo-test.ird.fr:84/cgi-bin/pathogen_Geographie.html' width='100%' height='650' style='border:solid 0px black;'></iframe>";
	#print "</div>";
	#print "</div>";
	#
	#print "<div id=\"middle\"></div>";
	#
	#print "<div id='right'>";
	#print "<div id='circle'>";
	#print "<iframe src='http://bioinfo-test.ird.fr:84/cgi-bin/slides/index.html' width='100%' height='650' style='border:solid 0px black;'></iframe>";
	#print "</div>";
	#print "</div>";
	#print "</div>";
	
	print "<p>
	<u><strong><font size='3' color='#550'>Fundings</font></strong></u>
	<br/><br/>
	This development was supported and financed by: 
	<ul>
	<li>System Directorate of Information <a href='https://www.ird.fr/dsi/la-dsi/organigramme-trombino/s.i.l/sil-de-france-sud' target='_blank'> <font size='3' color='#550'><strong>(DSI)</strong></font></a> IRD Montpellier in 2015 as parts of <a href='https://www.ird.fr/informatique-scientifique/projet_afficher/162' target='_blank'><font size='3' color='#550'><strong>SPIRALES </strong></font></a> project.<br/></li>
	<li>The Global Rice Science Partnership <a href='http://www.grisp.net/main/summary' target='_blank'><font size='3' color='#550'><strong>(GRiSP)</strong></font></a> from January 2012 to January 2015 as parts of <a href='http://www.madagascar.ird.fr/les-activites/la-recherche3/madagascar/riz-et-pathogenes/menergep' target='_blank'><font size='3' color='#550'><strong> MENERGEP </strong></font></a> project.<br/></li>
	</ul> ";
	print "</p>";
	print "<br/><br/>";
	
	print "<p>
	<u><strong><font size='3' color='#550'>Partners</font></strong></u>
	<div align=\"justify\">
	<table>
	<tr>
	<td valign=\"center\" align=\"center\" width=\"1%\">
	<td valign=\"center\" align=\"center\" width=\"15%\"><a href=\"http://www.ird.fr\" target=\"_blank\"><img alt=\"IRD logo\" src=\"http://bioinfo-test.ird.fr:84/cgi-bin/logos/IRD_logo.gif\" height=\"50\"/></a></td>
	<td valign=\"center\" align=\"center\" width=\"20%\"><a href=\"http://africarice.org/\" target=\"_blank\"><img alt=\"AfricaRice logo\" src=\"http://bioinfo-test.ird.fr:84/cgi-bin/logos/AfricaRice_logo.jpg\" height=\"60\"/></a></td></td>
	<td valign=\"center\" align=\"center\" width=\"20%\"><a href=\"http://www.grisp.net/main/summary\" target=\"_blank\"><img alt=\"GRiSP logo\" src=\"http://bioinfo-test.ird.fr:84/cgi-bin/logos/GRiSP_logo.jpg\" height=\"70\"/></a></td></td>
	<td valign=\"center\" align=\"center\" width=\"20%\"><a href=\"http://www.cirad.fr/\" target=\"_blank\"><img alt=\"CIRAD logo\" src=\"http://bioinfo-test.ird.fr:84/cgi-bin/logos/CIRAD_logo.gif\" height=\"70\"/></a></td>
	</td>
	</tr>
	</table>
	</div>";
	print "</p>";
	print "<br/><br/>";
	
	print "</div>";
	print "</div>";
	
	print "</div>";
	####################################################################
        # Plants
        ####################################################################
        print "<div id='Plants'>";
	print "<br/><br/><br/>";
	
	print "<table class='overview'>";
	print "<tr>";
	print "<td>";
	print "<font>The plants tab is divided into two parts:<br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	- Left the hithmaps that can see the number of variety for each African country. <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	- Right statistics that show the number of variety for each pathogenic.</font>";
	print "</td>";
	print "</tr>";
	print "</table>";
	print "<br/><br/>";

	print "<div id='Global'>";
	print "<div id='left'>";
	print "<div id='circle'>";
	print "<iframe src='http://bioinfo-test.ird.fr:84/cgi-bin/highmaps.cgi' width='100%' height='700' style='border:solid 0px black;'></iframe>";	
	print "</div>";
	print "</div>";
	
	print "<div id='middle'></div>";
	
	print "<div id='right'>";
	print "<div id='circle'>";
	print "<iframe src='$Configuration::CGI_URL/chrom_viewer.cgi?session=4' width='100%' height='700' style='border:solid 0px black;'></iframe>";
	print "</div>";
	print "</div>";
	print "</div>";
	
	print "</div>";
	####################################################################
        # Pathogens
        ####################################################################
        print "<div id='Pathogens'>";
	print "<br/><br/><br/>";
	
	print "<table class='overview'>";
	print "<tr>";
	print "<td>";
	print "<font>The pathogenic tab is divided into two parts: <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	- Left a Google Maps with different color marker to see pathotypes of each country. <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	- Right a picture slideshow of pathogenic and corresponding syntomes.</font>";
	print "</td>";
	print "</tr>";
	print "</table>";
	print "<br/><br/>";
	
	print "<div id='Global'>";
	print "<div id='left'>";
	print "<div id='circle'>";
	print "<iframe src='http://bioinfo-test.ird.fr:84/cgi-bin/pathogen_Geographie.html' width='100%' height='700' style='border:solid 0px black;'></iframe>";
	print "</div>";
	print "</div>";
	
	print "<div id='middle'></div>";
	
	print "<div id='right'>";
	print "<div id='circle'>";
	print "<iframe src='http://bioinfo-test.ird.fr:84/cgi-bin/slides/carrousel.html' width='100%' height='700' style='border:solid 0px black;'></iframe>";
	print "</div>";
	print "</div>";
	print "</div>";
	
	print "</div>";
        ####################################################################
        # Basic Search tab
        ####################################################################
        print "<div id='Search'>";
        print "<form name='form_Search' method ='post' action ='home.cgi'>";
	print "<br/><br/>";
	print "<fieldset>";
	print "<legend><b>Search fields</b></legend>";
	##############  Table of pathogens with different phenotypes  ##############
	print "<table class='pathogens'>";
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
	print "</tr>";
	print "</table>";
	##############  Free search area by name of variety  ##############
	print "<br/>";
        print "<dt><strong>Input</strong></dt>";
        print "<table>";
	print "<tr>";
	print "<td valign=center>Enter a list of varieties";
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
	##############  Multiple select by species  ##############
        print "<br/>";
	print "<table>";
	print "<tr>";
	print "<td valign=center>Enter species name (".scalar keys(%hash_species).")";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "</td>";
	print "<td>";
	print "<select multiple name=species id=species size=3>\n";
	foreach my $species(sort keys(%hash_species)){
		print "<option value='$species'>$species</option>\n";
        }
        print "</select>";
	print "</td>";
	print "</tr>";
	print "</table>\n";
	##############  Multiple select by country variety  ##############
	print "<br/>";
	print "<table>";
	print "<tr>";
	print "<td valign=center> Country of varieties (".scalar keys(%hash_country).")";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "</td>";
	print "<td>";
	print "<select multiple name=country id=country size=15>\n";
        foreach my $country (sort keys(%hash_country)){
		print "<option value='$country'>$country</option>\n";
        }
        print "</select></td></tr></table>\n";
	##############  Multiple select by variety  ##############
    	print "<br/>";
	print "<table>";
	print "<tr>";
	print "<td valign=center>Enter varieties names  (".scalar keys(%hash_varietes).") ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "</td>";
	print "<td>";
	print "<select multiple name=variete id=variete size=15>\n";
        foreach my $variete(sort keys(%hash_varietes)){      
                print "<option value='$variete'>$variete</option>\n";
        }
        print "</select>";
	print "</td>";
	print "</tr>";
	print "</table>\n";
        print "<br/><br/>";
	print "<input type='button' class='submit' value='Search' onclick='getSearch(\"$Configuration::CGI_URL/display_ajax.cgi\");'/>";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
	print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ";
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
	print "</div>";
	
        #####################################################################
        # Advanced Search tab
        #####################################################################
        print "<div id='Advanced' >";
	##############  Start of  form tag  ##############
        print "<form name='form_Advanced' method ='post' action ='home.cgi'>";
	print "<br/><br/>";
        print "<fieldset>";
	print "<script type='text/javascript'>var counter=0;</script>";
        print "<legend><b>Search fields</b></legend>";
	print "<br/><br/>";
	my %hash_interaction_type = ("R"=> "R", "MR"=> "MR", "S"=>"S");
	
	##############  Headline of the table  ##############
	print "<table id='mytable' border='1' CELLSPACING='0' width='90em 10%'>";
	print "<tr>";
	print "<th colspan='3'>Plant</th>";
	print "<th colspan='3'>Pathogen</th>";
	print "<th colspan='1'>Interactions</th>";
	print "</tr>";
	print "<th>Species</th>";
	print "<th>Country of variety</th>";
	print "<th>Variety</th>";
	print "<th >Pathogen</th>  "; 
	print "<th>Country of pathogen</th>";
	print "<th>Pathotype</th> ";
	print "<th>Interactions type</th>";
	print "<tr id='0'>";  
	
	###########################  Part Plante  ###########################
	##############  Species span  ##############
	print "<td align=center>";
	#print "<select name=0 id=species2_0 onChange='getCountryVarieties(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");getVarieties1(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\")'>\n";
	print "<select name=0 id=species2_0 onChange='getCountryVarieties(this.name);getVarieties1(this.name)'>\n";
	print "<option value='All'>All</option>\n";
	foreach my $species(sort keys(%hash_species)){
		print "<option value='$species'>$species</option>\n";
        }
	print "</select>\n";
	print "</td>";
	
	##############  Country_varietes span  ##############
	print "<td align=center><span id='PaysdesVarietesSpan_0'>\n"; 
	#print "<select name=0 id=country_varieties_0 onChange='getVarieties2(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
	print "<select name=0 id=country_varieties_0 onChange='getVarieties2(this.name);'>\n";
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
	##############  Pathogens span  ##############
	print "<td align=center><span id='PathogenesSpan_0'>";
	#print "<select name=0 id=pathogen_0 onChange='getCountryPathogenes(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");getPathotype1(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
	print "<select name=0 id=pathogen_0 onChange='getCountryPathogenes(this.name);getPathotype1(this.name);'>\n";
	print "<option value='All'>All</option>\n";
        foreach my $pathogen(sort keys(%pathogen)){      
		if ($pathogen){print "<option value='$pathogen'>$pathogen</option>\n";}
        }
	print "</select></span>\n";
	print "</td>";
	
	##############  Country_pathogens span  ##############
	print "<td align=center><span id='CountryPathogenesSpan_0'>\n";
	#print "<select name=0 id=country_pathogenes_0 onChange='getPathotype2(this.name,\"$Configuration::CGI_URL/display_ajax.cgi\");'>\n";
	print "<select name=0 id=country_pathogenes_0 onChange='getPathotype2(this.name);'>\n";
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
	print "</tr>";	
	print "</table>";
	##############  End of table  ##############
	
        print "<input type='button' value='+' style='left:90%; position:absolute;' onclick='counter++;addField(counter);'/></br></br>";  
	print "<input type='button' value='-' style='left:90%; position:absolute;' onclick='counter--;removeField(counter);'/></br></br>";
	my @TabOperator = ("And", "Or", "Nor");
	print "<select name=operator id=operator style='left:90%; position:absolute;'>\n";
        foreach my $operator (@TabOperator){
		if ($operator =~ /Or/) {
			print "<option value='Or' selected>Or</option>";
		}
		else{
			print "<option value='$operator'>$operator</option>";
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
        
	
#	print "<fieldset>";
#        print "<legend><b>Results display</b> </legend><br/><br/>";
#        print "<div id='results_Advanced1'></div>";
#        print "</fieldset>";
        
#	print "<fieldset>";
#        print "<legend><b>Results display</b> </legend><br/><br/>";
#        print "<div id='results_Advanced2'></div>";
#        print "</fieldset>";
	
#	print "<fieldset>";
#        print "<legend><b>Results display</b> </legend><br/><br/>";
#        print "<div id='results_Advanced3'></div>";
#        print "</fieldset>";
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
	my $cookie = $cgi->cookie( -name => $session );
	my $file_session = File::Spec->catfile( $session_dir, 'sess_' . $cookie );
	
	my $LOG = "$Configuration::TMP_DIR/log.info";
    open (F , ">", $LOG) or die ("erreur: \n $!\n");
	print F "no \n";
	
	if (  $cgi->request_method() eq 'POST' and $cgi->param('connexion') and ( $identifiant ne 'test' or $motdepasse ne 'pass' ) )
	{
		$message_erreur
		= "<p class='erreur center'>Erreur de connexion : identifiant ou mot de passe incorrect</p>";
	}
	
	elsif ( $cgi->request_method() eq 'POST' and $cgi->param('connexion') and ( $identifiant eq 'test' and $motdepasse eq 'pass' ) )
	{
		identifiant => $identifiant ;
		print $cgi->redirect('$Configuration::CGI_URL/file_upload.pl?session=$session');
		exit;
	}
	else {
	}
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
	
	close(F);
	if ($cgi -> param("mode") ne "simple"){	
	        print $footer;
	}
        print $cgi->end_html;
}

Display_InputForm();
