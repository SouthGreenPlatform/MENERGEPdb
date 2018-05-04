#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use Data::Dumper;
use JSON;

use Configuration;
require "manipulateBD.pl";
Parse_Files_List();
our %hash_varietes;
our %hash_pathogenes;
our %hash_interactions;

my %hash_coord;
#convert csv file into hash
my $File = "$Configuration::DATABASE_LOCATION/Countries.csv";
open (FILE, $File) or die "Could not open the file $!";
my $first_Line = 0;
my @Tab_header;
my @TabSyn;
my @Fields;
my $i;
my @Infos_line;		

while (my $line = <FILE>)
{
        chomp $line;
        if ($first_Line == 0)
        {
                @Tab_header = split/\t/, $line;
                $first_Line = 1;
                next;
        }
			
if ($Tab_header[0] =~ /country/)
{
        my $first_column_ref;
        my $column_name;
        @Infos_line = split /\t/, $line;
        $first_column_ref = $Infos_line[0];
        my $j = 1;
        foreach ($i = 1; $i <=$#Tab_header; $i++) 
        {
            $column_name = $Tab_header[$i]; 
            $hash_coord{$first_column_ref}{$column_name} = $Infos_line[$i];
            $j++;	
        }			
}
}

my $cgi = CGI->new;
#print "Content-type:  text/html\n\n";
print $cgi->header(-charset => 'utf-8', -lang => 'fr');
print <<"HEAD";
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>PathostDB - Localisation géographique des pathotypes</title>
    </head>

    <body>

<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=places&key=AIzaSyB47zwOd1a0FFaDTgwpgVlTWS6AhkAXX5M "></script>
<script type="text/javascript">
HEAD



print "var markers = [ \n";
for my $key (sort keys %hash_pathogenes){
    if (($hash_pathogenes{$key}{'Longitude'} ne "-") or ($hash_pathogenes{$key}{'Latitude'} ne "-")){
        print "{ \n";
        print "\t\"country\" :\"$hash_pathogenes{$key}{'Country'}\", \n";
        print "\t\"latitude\" : \"$hash_pathogenes{$key}{'Latitude'}\",\n";
        print "\t\"longitude\" : \"$hash_pathogenes{$key}{'Longitude'}\",\n";
        print "\t\"type\" :\"$hash_pathogenes{$key}{'Type'}\", \n";
        print "\t\"title\" : \"$key\", \n";
        print "}, \n";
    }
    for my $cle (sort keys %hash_coord){
        if (($hash_pathogenes{$key}{'Longitude'} eq "-") or ($hash_pathogenes{$key}{'Latitude'} eq "-")){
            if ($hash_pathogenes{$key}{'Country'} eq $hash_coord{$cle}{'name'}){
                $hash_pathogenes{$key}{'Longitude'} = $hash_coord{$cle}{'longitude'};
                $hash_pathogenes{$key}{'Latitude'} = $hash_coord{$cle}{'latitude'};
                print "{ \n";
                print "\t\"country\" :\"$hash_pathogenes{$key}{'Country'}\", \n";
                print "\t\"latitude\" : \"$hash_pathogenes{$key}{'Latitude'}\",\n";
                print "\t\"longitude\" : \"$hash_pathogenes{$key}{'Longitude'}\",\n";
                print "\t\"type\" :\"$hash_pathogenes{$key}{'Type'}\", \n";
                print "\t\"title\" : \"$key\", \n";
                print "}, \n";
            }
        }
    }    
}

print "   ]; \n";


print <<"BODY1";
window.onload = function () {

    var mapOptions = {
        center: new google.maps.LatLng(markers[0].latitude, markers[0].longitude),
        zoom: 4,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var infoWindow = new google.maps.InfoWindow();
    var latlngbounds = new google.maps.LatLngBounds();
    var map = new google.maps.Map(document.getElementById("dvMap"), mapOptions);
    var i = 0;
    var interval = setInterval(function () {
        var data = markers[i]
        var myLatlng = new google.maps.LatLng(data.latitude, data.longitude);
        var icon = "";
        
        icon = "http://maps.google.com/mapfiles/ms/icons/red.png";
        var marker = new google.maps.Marker({
            position: myLatlng,
            map: map,
            title: data.title,
            animation: google.maps.Animation.DROP,
            icon: new google.maps.MarkerImage(icon)
        });
        (function (marker, data) {
            google.maps.event.addListener(marker, "click", function (e) {
                infoWindow.setContent(data.type);
                infoWindow.open(map, marker);
            });
        })(marker, data);
        latlngbounds.extend(marker.position);
        i++;
        if (i == markers.length) {
            clearInterval(interval);
            var bounds = new google.maps.LatLngBounds();
            map.setCenter(latlngbounds.getCenter());
            map.fitBounds(latlngbounds);
        }
    }, 80);
}

</script>
<table>
<tr>
    <td>
        <div id="dvMap" style="width: 500px; height: 500px">
        </div>
    </td>
</tr>
</table>
</body>

</html>
BODY1
print $cgi->end_html;
