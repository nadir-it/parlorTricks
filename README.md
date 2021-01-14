# parlorTricks
<img src="https://raw.githubusercontent.com/nadir-it/parlorTricks/main/GPSMetaData.jpeg" width="80%">

## Converting 250,000 JSON files to a CSV of GPS data then plotting that data in R.

### massive_grep.sh 
Massive_grep.sh was used to comb through approximately 250,000 JSON files worth of metadata.
This resulted in a directory filled with just under 70,000 files with GPS metadata in JSON format.

### scrape.py
Scrape.py was then used to extract as many useful coordinates as possible and store them in a CSV file.

### parlorTrick.R
ParlorTrick.R processed this data, and isolated United States based coordinates to generate a point map.
This script was made possible on a short notice by tidyverse and ggmap.


