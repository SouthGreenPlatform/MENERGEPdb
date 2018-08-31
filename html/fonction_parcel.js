/*************
fonction.js
***************
Version: 0.1
Date:    01/04/2016
Author:  Khoudia Fall && Maira Barca
Contains various helper functions.





/**
******************************************************************************************************************************************
* Function afficheSynonymes_varietes() give the alert for the synonyms in the Basic Search tab
******************************************************************************************************************************************
**/
function afficheSynonymes_varietes(synonymes)
{
        var list_varietes = "Synonyms for this variety : " + synonymes + "\n";
        alert (list_varietes);
}

/**
*****************************************************************************************************
* Function afficheIsolat() give the alert for the different pathotypes in the Basic Search tab
*****************************************************************************************************
**/
function afficheIsolat(phenotypes,varCod)
{
	var list_isolat = "The phenotypes of isolates tested in " +varCod+ " are :  "+phenotypes+"\n";
	alert (list_isolat);
}

/**
*****************************************************************************************************
* Function afficheSource() give reference for the interaction information in advanced tab
*****************************************************************************************************
**/
function afficheSource(source)
{
	var ref = "Publication : " +source;
	alert (ref);
}


/**
**********************************************************************
* Function addField() allows the cloning of the div 'divAutomatique'
**********************************************************************
**/
function addField(counter){    
	var myDiv = document.getElementById("0");
	var divClone = myDiv.cloneNode(true);
	divClone.id = counter;
	
	var elms = divClone.getElementsByTagName("*");
	for (var i = 0; i < elms.length; i++) {
	  if (elms[i].id == "species2_0") {
	    elms[i].id = "species2_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "country_varieties_0") {
	    elms[i].id = "country_varieties_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "PaysdesVarietesSpan_0") {
	    elms[i].id = "PaysdesVarietesSpan_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "VarietesSpan_0") {
	    elms[i].id = "VarietesSpan_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "pathogen_0") {
	    elms[i].id = "pathogen_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "country_pathogenes_0") {
	    elms[i].id = "country_pathogenes_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "CountryPathogenesSpan_0") {
	    elms[i].id = "CountryPathogenesSpan_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "pathotype_0") {
	    elms[i].id = "pathotype_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "PathotypeSpan_0") {
	    elms[i].id = "PathotypeSpan_" + counter;
	    elms[i].name = counter;
	  }
	  if (elms[i].id == "interaction_type_0") {
	    elms[i].id = "interaction_type_" + counter;
	    elms[i].name = counter;
	  }
	}
	mytable.appendChild(divClone); 

}
/**
**********************************************************************
* Functions removeField() allows the deletion of the last cloned div 
**********************************************************************
**/
function removeField(counter){
	var myDyv = document.getElementById(counter);
	while (myDyv.lastChild) {
	  var oldDiv = myDyv.removeChild(myDyv.lastChild);
	}
}


//
/**
**********************************************************************
* Functions to upload fields in Basic tab
**********************************************************************
**/

function update_countries(url)
{
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changeCountryBasic";
	params = params + "&counter=0";
	listelements = document.getElementById("species1_0").value;
      	if (listelements){
                params = params + '&ListElements=' + listelements;
        }

	//console.log(params);
	url = url + "?" + params;
	var ajax_div = document.getElementById('country1_0');
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 
}

function update_var(url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changeVarBasic";
	params = params + "&counter=0";
	listelements = document.getElementById("species1_0").value + ",";
      	if (listelements){
                params = params + '&ListElements=' + listelements;
        }


	//console.log(params);
	url = url + "?" + params;
	var ajax_div = document.getElementById('variete1_0');
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 
}


function updateVar2(url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changeVar2Basic";
	params = params + "&counter=0";
	listelements = document.getElementById("species1_0").value + "," + document.getElementById("country1_0").value;
      	if (listelements){
                params = params + '&ListElements=' + listelements;
        }
	console.log(params);
	url = url + "?" + params;
	var ajax_div = document.getElementById('variete1_0');
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 
}

function update_date(url){
	var params = "action=changeDate";
	params = params + "&counter=0";
	listelements = document.getElementById("species1_0").value + ",";
      	if (listelements){
                params = params + '&ListElements=' + listelements;
        }


	console.log(params);
	url = url + "?" + params;
	var ajax_div = document.getElementById('date1_0');
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 	
	
}

function update_date2(url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changeDate2";
	params = params + "&counter=0";
	listelements = document.getElementById("species1_0").value + "," + document.getElementById("country1_0").value;
      	if (listelements){
                params = params + '&ListElements=' + listelements;
        }
	//console.log(params);
	url = url + "?" + params;
	var ajax_div = document.getElementById('date1_0');
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 
}
/**
**********************************************************************
* Functions to upload fields in Advanced tab
**********************************************************************
**/
//Plant tab
function getCountryVarieties(counter,url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changeCountry";
	params = params + "&counter="+counter;
	listelements = document.getElementById("species2_"+counter).value;
	if (listelements){
                params = params + '&ListElements=' + listelements;
        }	
	url = url + "?" + params;
	var ajax_div = document.getElementById('PaysdesVarietesSpan_'+counter);
	$.get( url, function( data ) {
		      ajax_div.innerHTML = data;
	       });
}

function getVarieties1(counter,url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changeVarieties1";
	params = params + "&counter="+counter;
	listelements = document.getElementById("species2_"+counter).value + ",";
      	if (listelements){
                params = params + '&ListElements=' + listelements;
        }
	url = url + "?" + params;
	var ajax_div = document.getElementById('VarietesSpan_'+counter);
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 
}

function getVarieties2(counter, url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changeVarieties2";
	params = params + "&counter="+counter;
	listelements = document.getElementById("species2_"+counter).value + "," + document.getElementById("country_varieties_"+counter).value;
      	if (listelements){
                params = params + '&ListElements=' + listelements;
        }
	url = url + "?" + params;
	var ajax_div = document.getElementById('VarietesSpan_'+counter);
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 
}

//Pathogen tab
function getCountryPathogenes(counter,url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changeCountryPathogenes";
	params = params + "&counter="+counter;
	listelements = document.getElementById("pathogen_"+counter).value;
	if (listelements){
                params = params + '&ListElements=' + listelements;
				//console.log(listelements);
        }
	url = url + "?" + params;
	var ajax_div = document.getElementById('CountryPathogenesSpan_'+counter);
	$.get( url, function( data ) {
		      ajax_div.innerHTML = data;
	       });
}

function getPathotype1(counter,url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changePathotype1";
	params = params + "&counter="+counter;
	listelements = document.getElementById("pathogen_"+counter).value + ",";
      	if (listelements){
                params = params + '&ListElements=' + listelements;
        }
	url = url + "?" + params;
	var ajax_div = document.getElementById('PathotypeSpan_'+counter);
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 
}

function getPathotype2(counter,url){
	//var url = "http://localhost/cgi-bin/menergepdb-work/display_ajax.cgi";
	var params = "action=changePathotype2";
	listelements = document.getElementById("pathogen_"+counter).value + "," + document.getElementById("country_pathogenes_"+counter).value;
	if (listelements){
                params = params + '&ListElements=' + listelements;
        }
	url = url + "?" + params;
	var ajax_div = document.getElementById('PathotypeSpan_'+counter);
	$.get( url, function( data ) {
			ajax_div.innerHTML = data;
	       }); 
}

/**
 **
***************************************************************************************************
* Functions getBasic2() gere tous les requettes de l'onglet  
***************************************************************************************************
**/
function getBasic2(url,session){
	//alert(bouclade);

	var params = "action=getBasic2"+ session;
	//params = params + '&'+ session;
	var ajax_div = document.getElementById('results_Search');
    var counter = 0;
	var Pathogens = document.forms.form_Search.PathogenNames.value;
	var arrayOfStrings = Pathogens.split(";");
	
	for (var i = 0; i <= arrayOfStrings.length; i++)
	{
		var params_res;
		for (var e = 0; e <= document.getElementsByName(Pathogen).length; e++)
		{
			var Pathogen = arrayOfStrings[i];
			var list_Pathotype="";
			for (var j = 0; j < document.getElementsByName(Pathogen).length; j++)
			{
				if (document.getElementsByName(Pathogen)[j].checked == true)
				{
					list_Pathotype += document.getElementsByName(Pathogen)[j].value + ",";
					//recuperation de la valeur (R, MR, S)
					
				}
			}
			params_res = 'resistance_'+Pathogen+'=' + list_Pathotype;			
		}
		params = params + '&'+ params_res;
		
		console.log(params);
		//action getSearch sur le pathogene selectionne
		//action=getSearch&resistance_RYMV=R,&resistance_Xanthomonas=&resistance_undefined=
		
	}
	
		if (document.getElementById('species1_'+counter).options)
		{
			var list = document.getElementById('species1_'+counter).options;
			var list_species2="";
			for (var i = list.length - 1; i>=0; i--)
			{
				if (document.getElementById('species1_'+counter).options[i].selected==true){
					list_species2 += list[i].value + ","; 
				}
			}
			params = params + '&species1_'+counter +'='+ list_species2;
		}

		if (document.getElementById('country1_'+counter).options)
		{
			var list = document.getElementById('country1_'+counter).options;
			var list_country_variete="";
			for (var i = list.length - 1; i>=0; i--)
			{
			      if (document.getElementById('country1_'+counter).options[i].selected==true){
					list_country_variete += list[i].value + ",";
				}
			}
			params = params + '&country1_'+counter +'=' + list_country_variete;
		}
      
		if (document.getElementById('variete1_'+counter).options)
		{
			var list = document.getElementById('variete1_'+counter).options;
			var list_variete2="";
			for (var i = list.length - 1; i>=0; i--)
			{
				if (document.getElementById('variete1_'+counter).options[i].selected==true){
					list_variete2 += list[i].value + ",";
				}
			}
			params = params + '&variete1_'+counter +'=' + list_variete2;
		}
		
		if(document.getElementById('date1_'+counter) != null){
			if (document.getElementById('date1_'+counter).options)
			{
				var list = document.getElementById('date1_'+counter).options;
				var list_year="";
				for (var i = list.length - 1; i>=0; i--)
				{
					  if (document.getElementById('date1_'+counter).options[i].selected==true){
						list_year += list[i].value + ",";
					}
				}
				params = params + '&date1_'+counter +'=' + list_year;
			}
		}
	
	Vars = document.forms.form_Search.var.value;
        if (Vars)
	{		
		var res = Vars;
                params = params + '&var=' + res;
				console.log(params);
	}
	
	url = url + "?" + params;
	console.log(url);
	console.log(session);
	$.get( url, function( data ) {
		ajax_div.innerHTML = data;
	});
}

/**
 **
***************************************************************************************************
* Functions getAdvanced() gere tous les requettes de l'onglet  Multipathogen Advanced search
***************************************************************************************************
**/
function getAdvanced(bouclade,url, session){
	//alert(bouclade);
	
	var params = "action=getAdvanced"+ session;
	//params = params + '&session2='+ session;
	var ajax_div = document.getElementById('results_Advanced');
	for (var counter=0; counter <= bouclade; counter++)
	{	
		if (document.getElementById('species2_'+counter).options)
		{
			var list = document.getElementById('species2_'+counter).options;
			var list_species2="";
			for (var i = list.length - 1; i>=0; i--)
			{
				if (document.getElementById('species2_'+counter).options[i].selected==true){
					list_species2 += list[i].value + ","; 
				}
			}
			params = params + '&species2_'+counter +'='+ list_species2;
		}

		if (document.getElementById('country_varieties_'+counter).options)
		{
			var list = document.getElementById('country_varieties_'+counter).options;
			var list_country_variete="";
			for (var i = list.length - 1; i>=0; i--)
			{
			      if (document.getElementById('country_varieties_'+counter).options[i].selected==true){
					list_country_variete += list[i].value + ",";
				}
			}
			params = params + '&country_varieties_'+counter +'=' + list_country_variete;
		}
      
		//if (document.getElementById('variety2_'+counter).options)
		if (document.getElementById('variety2_0').options)
		{
			var list = document.getElementById('variety2_0').options;
			var list_variete2="";
			for (var i = list.length - 1; i>=0; i--)
			{
				if (document.getElementById('variety2_0').options[i].selected==true){
					list_variete2 += list[i].value + ",";
				}
			}
			params = params + '&variety2_'+counter +'=' + list_variete2;
		}
		
		if (document.getElementById('pathogen_'+counter).options)
		{
			var list = document.getElementById('pathogen_'+counter).options;
			var list_pathogen="";
			for (var i = list.length - 1; i>=0; i--)
			{
				if (document.getElementById('pathogen_'+counter).options[i].selected==true){
					list_pathogen += list[i].value + ",";
				}
			}
			params = params + '&pathogen_'+counter +'=' + list_pathogen;
		}

		if (document.getElementById('country_pathogenes_'+counter)){
		if (document.getElementById('country_pathogenes_'+counter).options)
		{
			var list = document.getElementById('country_pathogenes_'+counter).options;
			var list_country_pathogenes="";
			for (var i = list.length - 1; i>=0; i--)
			{
				if (document.getElementById('country_pathogenes_'+counter).options[i].selected==true){
					list_country_pathogenes += list[i].value + ",";
				}
			}
			params = params + '&country_pathogenes_'+counter +'=' + list_country_pathogenes;
		}
		}
	
      if (document.getElementById('pathotype_'+counter)){
		if (document.getElementById('pathotype_'+counter).options)
		{
			var list = document.getElementById('pathotype_'+counter).options;
			var list_pathotype="";
			for (var i = list.length - 1; i>=0; i--)
			{
				if (document.getElementById('pathotype_'+counter).options[i].selected==true){
					list_pathotype += list[i].value + ",";
				}
			}
			params = params + '&pathotype_'+counter +'=' + list_pathotype;
		}	
	  }
	  
		if (document.getElementById('interaction_type_'+counter).options)
		{
			var list = document.getElementById('interaction_type_'+counter).options;
			var list_interaction_type="";
			for (var i = list.length - 1; i>=0; i--)
			{
			      if (document.getElementById('interaction_type_'+counter).options[i].selected==true){
					list_interaction_type += list[i].value + ",";
				}
			}
			params = params + '&interaction_type_'+counter +'=' + list_interaction_type;
		}
		
		if (document.getElementById('operator_'+counter)){		
		if (document.getElementById('operator_'+counter).options)
		{
		
			var list = document.getElementById('operator_'+counter).options;
			var list_operator="";
			for (var i = list.length - 1; i>=0; i--)
			{
			      if (document.getElementById('operator_'+counter).options[i].selected==true){
					list_operator += list[i].value + ",";
				}
			}
			params = params + '&operator_'+counter +'=' + list_operator;
			//alert(params);
		}
		}
		
	}
	console.log(params);
	params = params + '&counter='+counter;
	url = url + "?" + params;
	$.get( url, function( data ) {
	  ajax_div.innerHTML = data;
	});
}

