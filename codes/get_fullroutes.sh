#!/bin/sh
# need the date of 2 days before
Y=$(date --date="2 day ago" +'%Y')
M=$(date --date="2 day ago" +'%m')
MD=$(date --date="2 day ago" +"%m%d")

# for 00:00, 08:00, 16:00 in a day

# downloading a file from a GMT +1 time zone machine...?
eval wget -O /var/jpnic/data/routes/mrt/bview.${Y}${MD}.0000.gz http://data.ris.ripe.net/rrc06/${Y}.${M}/bview.${Y}${MD}.0000.gz
# bgpdump the donwloaded file to convert it into an text file
eval /usr/local/bin/bgpdump -M "/var/jpnic/data/routes/mrt/bview.${Y}${MD}.0000.gz" > "/var/jpnic/data/routes/txt_format/fullroute_${Y}${MD}.0000"

eval wget -O /var/jpnic/data/routes/mrt/bview.${Y}${MD}.0800.gz http://data.ris.ripe.net/rrc06/${Y}.${M}/bview.${Y}${MD}.0800.gz
eval /usr/local/bin/bgpdump -M "/var/jpnic/data/routes/mrt/bview.${Y}${MD}.0800.gz" > "/var/jpnic/data/routes/txt_format/fullroute_${Y}${MD}.0800"

eval wget -O /var/jpnic/data/routes/mrt/bview.${Y}${MD}.1600.gz http://data.ris.ripe.net/rrc06/${Y}.${M}/bview.${Y}${MD}.1600.gz
eval /usr/local/bin/bgpdump -M "/var/jpnic/data/routes/mrt/bview.${Y}${MD}.1600.gz" > "/var/jpnic/data/routes/txt_format/fullroute_${Y}${MD}.1600"
