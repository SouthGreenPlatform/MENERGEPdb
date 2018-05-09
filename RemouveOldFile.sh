#Ce script efface les fichiers vieux de plus 100 jours dans le repertoire tmp et ses sous repertoire.
#!/bin/bash
find /var/www/html/tmp/ -type f -mtime +100 -exec /bin/rm -f {} \;
