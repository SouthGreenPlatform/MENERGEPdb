#!/usr/bin/perl
use warnings;
use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use File::Spec;
use Data::Dumper;

use Configuration;

my $cgi = CGI->new;
my $session = $cgi->param('session');
my $session_dir = "$Configuration::HTML_DIR/tmp/";

our $level_user;


my $good_identifiant = 'test';
my $good_password  = 'pass';


my $identifiant    = $cgi->param('identifiant');
my $motdepasse       = $cgi->param('motdepasse');
my $message_erreur = '';

my $cookie = $cgi->cookie( -name => $session );
my $file_session = File::Spec->catfile( $session_dir , 'sess_' . $cookie );


print $cgi->header( -charset => 'utf-8', -lang => 'fr' );
print $cgi->start_html(
  -title => "MENERGEPdb: Login ",
  #-style => { 'src' => 'http://bioinfo-test.ird.fr:84/cgi-bin/css/style.css'}, <!-- '/sessions/style.css' }, -->
  -style => { 'src' => '$Configuration::CSS_URL/css/style.css'}, <!-- '/sessions/style.css' }, -->
);

print <<"RESUME";

<br/><br/><br/><br/><br/><br/>

<body class="login">
<center>
<!-- <h1 class="center"><font color='red'>Failed Authentification</font></h1> -->
<p>Username or Password incorrect. Please <br/> try again.</p><br/>  

<form accept="text/html" method="POST" accept-charset="utf-8" action="login.cgi" name="formulaire">

<table CELLSPACING='0' class='login'>
<tr>
<th bgcolor="#006800" colspan='3'><font color='red'>Failed Authentification</font></th>
</tr>

<tr>
<td>User Name:</td>
<td><input name="identifiant" type="text" size="50"></td>
</tr>

<tr>
<td>Password:</td>
<td><input name="motdepasse" type="password" size="50"></td>
</tr>

<tr>
<td colspan="2" style="padding-top:20px;text-align:center;">
<input name="connexion" type="submit" value="Login"> 
</td>
</tr>

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

<center>


RESUME

if ( defined $message_erreur ) { print $message_erreur; }

print $cgi->end_html;