#Ce script deplace les fichiers .csv uploades du repertoire source vers le repertoire de destination
#!/bin/bash
source=/var/www/html/tmp/tmp_Repository/                       
destination=/var/www/cgi-bin/Documents/

if [ -d $source ] && [ -d $destination ]
        then
               echo "Les deux chemins sont bon"
        else
               echo "un des chemins n'est pas bon"
fi

cd $source        

for i in `ls`        

do
        if [[ $i = *.csv.* ]]    
                then
                        mv $i $destination/$i            
                else

                if [ -d $i ]                                 
                        then
                                cd $i                         
                                for j in `ls`                 
                                do
                                        if [[ $j = *.csv.* ]]       
                                               then
                                                        mv $j $destination/$j

                                                        echo "$j"
                                        fi
                                done
                        cd ..            
                fi
        fi
done
 

