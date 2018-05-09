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

my $header = qq~

~;

my $footer = qq~

~;

# params

####################
my $SCRIPT_NAME = "highmaps.cgi";

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
        print $cgi->start_html(
                -title  => "MENERGEPdb",
                -meta   => {'keywords'=>'Riz Africain, Phytopathogénes','description'=>'Database for Plant-Pathogen Interaction analysis'},
                -script => [

                                {'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/javascript2/jquery-1.4.4.min.js"},
				
                                {'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/highmaps.js"},
				{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/africa.js"},
				{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/south-america.js"},
				 {'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/world.js"},
                              	{'language'=>'javascript', 'src'=>"$Configuration::HTML_URL/highmaps/exporting.js"},
                                
		],

               -style  => [
                                {'src'=>,"$Configuration::HTML_URL/css/style.css",'type'=>'text/css'},
				]
        );

        print $header;

#############################
require "manipulateBD.pl";
Parse_Files_List();

our %hash_varietes;

my %hash_variety_country;
foreach my $variete (sort keys(%hash_varietes))
{
	my $country_name = $hash_varietes{$variete}{"Country"};
        $hash_variety_country{$variete} = $hash_varietes{$variete}{"Country"};
}
#print Dumper (\%hash_variety_country);

my %countries;
foreach my $variete (sort keys(%hash_variety_country))
    {
	my $country = $hash_variety_country{$variete};
	$countries{$country}++;
    }
my $data = "";
foreach my $country(keys(%countries)){
	my $nb = $countries{$country};
	$data .= "{\"name\": \"$country\",\"value\": $nb},";
}
    
###############################

        my $tab = qq~
<script>
\$(function () {

    var data = [$data];
    \$('#container').highcharts('Map', {

        title : {
            text : 'Number of varieties per country'
        },

        subtitle : {
            text : 'Source map: CIAT'
        },

        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },
        colorAxis: {
            min: 0
        },
        series : [{
            data : data,
            mapData: Highcharts.maps['custom/world'],
            joinBy: 'name',
            name: 'Nb of varieties',
            states: {
                hover: {
                    color: '#6B8E23'
                }
            },
            dataLabels: {
                enabled: true,
                format: '{point.name}'
            }
        }]
    });
});
</script>

~;

        print $tab;

        print "<div id='container' style='height: 800px; min-width: 310px; max-width: 800px; margin: 0 auto'>";
        
        print $footer;
        print $cgi->end_html;
}

Display_InputForm();
