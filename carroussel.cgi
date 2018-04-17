#!/usr/bin/perl
use strict;
use CGI;
use Data::Dumper;
use Configuration;


#search images that will appear in carroussel
my @files;
my $link = "$Configuration::HTML_URL/slides/img_carrousel/"; 
my $rep = "$Configuration::HTML_DIR/slides/img_carrousel";
opendir(REP,$rep) or die "Error : $!\n"; 

while(defined(my $fic=readdir REP)){
    my $f="$fic";
    if(($fic=~/.*\.jpg/) || ($fic=~/.*\.png/) || ($fic=~/.*\.jpeg/)){
        push(@files, $f);
    }
}
closedir(REP);


#html page
my $cgi = CGI->new;
print "Content-type:  text/html\n\n";
print <<"HEAD";
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>

HEAD

print "<body>";
print "\n";
print "<div class=\"container\">";
print "\n";
print "<div id=\"myCarousel\" class=\"carousel slide\" data-ride=\"carousel\">";
print "\n";
print "<!-- Indicators -->";
    print "\n";
    print "<ol class=\"carousel-indicators\">";
    print "\n";
    print "<li data-target=\"#myCarousel\" data-slide-to=\"0\" class=\"active\"></li>";
    print "\n";
    for (my $i=1;($i<= scalar(@files)-1);$i++){
    print "<li data-target=\"#myCarousel\" data-slide-to=\"$i\"></li>";
    print "\n";
    }
    print "</ol>";
    print "\n";

    print "<!-- Wrapper for slides -->";
    print "\n";
    print "<div class=\"carousel-inner\">";
    print "\n";
      
    print "<div class=\"item active\">";
    print "\n";
    print "<img src=\"$link@files[0]\" alt=\"@files[0]\" style=\"width:100%;\"> ";
    print "\n";
    print "</div>";
    print "\n";
    for (my $i=1;($i<= scalar(@files)-1);$i++){
    print "<div class=\"item\">";
    print "\n";
    print "<img src=\"$link@files[$i]\" alt=\"@files[$i]\" style=\"width:100%;\">";
    print "\n";
    print "</div>";
    print "\n";
    }
    
print <<"BODY";
    <!-- Left and right controls -->
    <a class="left carousel-control" href="#myCarousel" data-slide="prev">
      <span class="glyphicon glyphicon-chevron-left"></span>
      <span class="sr-only">Previous</span>
    </a>
    <a class="right carousel-control" href="#myCarousel" data-slide="next">
      <span class="glyphicon glyphicon-chevron-right"></span>
      <span class="sr-only">Next</span>
    </a>
  </div>
</div>

</body>
</html>

BODY
print $cgi->end_html;