#!/usr/bin/perl

use strict;
use warnings;
use Carp qw (cluck confess croak);

use CGI;
use Configuration;

my $cgi = CGI->new();


my $display = $cgi -> param('display');
my $session = $cgi -> param('session');
my $variete = $cgi -> param('variete');


my $config;
my $execution_dir = "$Configuration::TMP_DIR";
if ($session)
{
	$config = "$execution_dir/tables.$session.conf";
}
my %CONFIG;
eval '%CONFIG = ( ' . `cat $config` . ')';
die "Error while loading configuration file: $@n" if $@;


my $javascript_url = $Configuration::JAVASCRIPT_URL;
my $json_dir = $Configuration::JSON_DIR;
my $json_url = $Configuration::JSON_URL;
my $html_dir = $Configuration::HTML_DIR;
my $tmp_url = $Configuration::TMP_URL;

print $cgi->header();

print $cgi->start_html(
	-title  => "Table viewer",
        -style  => [{'src'=>"$javascript_url/DataTables-1.10.7/examples/resources/syntax/shCore.css", 'type'=>'text/css'}, 
                    {'src'=>"$javascript_url/DataTables-1.10.7/media/css/jquery.dataTables.css", 'type'=>'text/css'},
                    {'src'=>"$javascript_url/DataTables-1.10.7/examples/resources/demo.css", 'type'=>'text/css'},
		],
	-script => [
                    {'-language'=>'javascript', '-src'=>"$javascript_url/DataTables-1.10.7/media/js/jquery.js"},
                    {'-language'=>'javascript', '-src'=>"$javascript_url/DataTables-1.10.7/media/js/jquery.dataTables.js"},
                    {'-language'=>'javascript', '-src'=>"$javascript_url/DataTables-1.10.7/examples/resources/demo.js"},
                    {'-language'=>'javascript', '-src'=>"$javascript_url/DataTables-1.10.7/examples/resources/syntax/shCore.js"},
                    {'-language'=>'javascript', '-src'=>"$Configuration::HTML_URL/fonctions.js"},

]

);


my $init = qq~
<script type="text/javascript" language="javascript" class="init">
\$(document).ready(function() {
	\$('#example').DataTable( {
        "ajax": '$json_url/table.$session.json'
    } );
} );
	</script>
~;

my $javascript = qq~

        <script type="text/javascript">

        function reload()
        {
                var display = document.getElementById('display').value;
                var session = document.getElementById('session').value;
                var url = window.location.href;
                var base_url = url.split('?');
                url = base_url[0];
                url += '?display='+display;
                url += '&session='+session;
                window.location.href = url;
        }

        </script>
~;

print $javascript;

#if (scalar keys(%CONFIG) > 1){
	print "Select the table to show: <select name='display' id='display' onchange='reload();'>";
	foreach my $key(sort keys(%CONFIG))
	{
		if (!$display){$display=$key;}
		my $select_title = $CONFIG{$key}{"select_title"};
		if ($display eq $key)
		{
			print "<option value='$key' selected=\"selected\">$select_title</option>\n";
		}
		else
		{
			print "<option value='$key'>$select_title</option>\n";
		}
	}
	print "</select>\n";
#}

print "<input type=\"hidden\" id=\"session\" value=\"$session\"> \n";


open(my $JSON,">$json_dir/table.$session.json");
print $JSON "{\n\"data\": [\n";
my $file = $CONFIG{$display}{"file"};
my $link = $CONFIG{$display}{"link"};
my $header = `head -1 $file`;
chomp($header);
my @infos_header = split(/\t/,$header);
$header = join("<\/th><th>",@infos_header);
open(my $F,$file) or print "Can not open file $file<br>";
<$F>;
my @table_fields;
while(<$F>)
{
	my $line = $_;
	chomp($line);
	my @infos_line = split(/\t/,$line);
	my $field = "[\n\"";
	if ($link){
		my $id = shift(@infos_line);
		my ($chrom,$pos) = split(":",$id);
		my $start = $pos - 5000;
		my $end = $pos + 5000;
		my $link_jbrowse = $link . "&loc=$chrom:$start..$end&highlight=$chrom:$pos..$pos";
		$field .= "<a href=$link_jbrowse target=_blank>$id</a>\",\"";
	}
	$field .= join("\",\"",@infos_line);
	$field .= "\"\n]";
	push(@table_fields,$field);
}
close($F);
print $JSON join(",\n",@table_fields);
print $JSON "]\n}";
close($JSON);
print "<br/><br/>";

print $init;
my $table = qq~
<table id="example" class="display" cellspacing="0" width="100%">
				<thead>
					<tr>
						<th>$header</th>
					</tr>
				</thead>

				<tfoot>
					<tr>
						<th>$header</th>
					</tr>
				</tfoot>

				<tbody>
</tbody>
			</table>
~;
print $table;
print "<a href='$json_url/table.$session.json	' download> <button> Download result table in JSON format</button> </a>";
print "<a href='$tmp_url/table.$session.csv	' download> <button> Download result table in CSV format </button> </a>";
