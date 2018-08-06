#!/usr/bin/perl
#
#
use CGI;
use strict;
my $PROGNAME = "file_upload.cgi";
my $cgi = new CGI();
my $session = $cgi->param('session');
my $submitter = $cgi->param('submitter');
my $description = $cgi->param('description'); 

use Configuration; 
  
print "Content-type: text/html\n\n";



if (! $cgi->param("button") ) {
	DisplayForm();
	exit;
}
my $upfile = $cgi->param('upfile');


my $basename = GetBasename($upfile);
no strict 'refs';

#open(O, ">$Configuration::HTML_DIR/tmp/Upload/file") or print "error write";

if (! open(FILE, ">$Configuration::HTML_DIR/tmp/tmp_Repository/File.$submitter.$basename")) {
	print "Can't open var/www/html/tmp/tmp_Repository/ for writing - $!";
	exit(-1);
}


print "Saving the file to /tmp<br>\n";


my $nBytes = 0;
my $totBytes = 0;
my $buffer = "";
binmode($upfile);
while ( $nBytes = read($upfile, $buffer, 1024) ) {
	print FILE $buffer;
	$totBytes += $nBytes;
}

close(FILE);
use strict 'refs';
print "Thanks $submitter for uploading $basename ($totBytes bytes)<br>\n File description: $description";	
sub GetBasename {
	my $fullname = shift;

	my(@parts);
	if ( $fullname =~ /(\\)/ ) {
		@parts = split(/\\/, $fullname);
	} else {
		@parts = split(/\//, $fullname);
	}

	return(pop(@parts));
}
sub DisplayForm {
print <<"HTML";
<html>
<head>
<link rel="stylesheet" href="http://bioinfo-test.ird.fr:84/cgi-bin/css/style.css" />

<title>PathostDB: File Upload</title>

<center>
<br/><br/><br/><br/><br/><br/>
<p>This page allows you to upload new files of host-pathogen interactions <br/> to enrich the actual database.</p><br/>
<form method="post" action="$PROGNAME" enctype="multipart/form-data">
<table CELLSPACING='0' class='upload'>
<tr>
<th bgcolor="#006800" colspan='2'><font color='red'>Upload Form</font></th>
</tr>
<tr>
<td>Enter a csv file to upload :</td><td><input type="file" name="upfile"><br/></td>
</tr>
<tr></tr>
<!--
<tr>
<td>Private Access :</td><td><input type='radio' name='acces' value='' id='' checked/></td>
</tr>
<tr>
<td>Public Access :</td><td><input type='radio' name='acces' value='' id=''/></td> 
</tr>
-->
<tr></tr>
<tr>
<td>Submitter : </td><td><input type="text" name="submitter" placeholder="Your name" id="submitter"/></td>
</tr>
<tr>
<td>File description : </td><td><textarea name="description" id="description"></textarea></td>
<tr>
</tr>
<tr>
<td colspan="2" style="padding-top:20px;text-align:center;"><input type="submit" name="button" value="Upload File"></td>
</tr>

<!--  <tr>  <td colspan="2"><input type="hidden" name="session" value="$session"></td>  </tr>  -->
</table>
</form>

<br/><br/><br/><br/>

<p>
<div align="center">
<table><tr>
<td valign="center" align="center" width="10%">
<td valign="center" align="left" width="5%"><a href="http://www.ird.fr" target="_blank"><img alt="IRD logo" src="http://bioinfo-test.ird.fr:84/cgi-bin/logos/IRD_logo.gif" height="50"/></a></td>
<td valign="center" align="center" width="5%"><a href="http://www.umr-rpb.fr" target="_blank"><img alt="IPME logo" src="http://bioinfo-test.ird.fr:84/cgi-bin/logos/IPME_logo.png"height="60"/></a></td>
<td valign="center" align="center" width="5%"><a href="http://africarice.org/" target="_blank"><img alt="AfricaRice logo" src="http://bioinfo-test.ird.fr:84/cgi-bin/logos/AfricaRice_logo.jpg" height="60"/></a></td>
</td>
<td valign="center" align="center" width="5%"><a href="http://www.grisp.net/main/summary" target="_blank"><img alt="GRiSP logo" src="http://bioinfo-test.ird.fr:84/cgi-bin/logos/GRiSP_logo.jpg" height="70"/></a></td>
</td>
<td valign="center" align="center" width="5%"><a href="http://www.diade-research.fr/" target="_blank"><img alt="DIADE logo" src="http://bioinfo-test.ird.fr:84/cgi-bin/logos/DIADE_logo.png" height="65"/></a></td>
</td>
<td valign="center" align="center" width="5%"><a href="http://www.cirad.fr/" target="_blank"><img alt="CIRAD logo" src="http://bioinfo-test.ird.fr:84/cgi-bin/logos/CIRAD_logo.gif" height="70"/></a></td>
</td>
<td valign="center" align="center" width="10%">
</tr></table>
</div>
</p>

</center>

HTML
}
