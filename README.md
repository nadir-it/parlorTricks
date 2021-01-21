# parlorTricks
<img src="https://raw.githubusercontent.com/nadir-it/parlorTricks/main/GPSMetaData.jpeg" width="80%">

## Converting 250,000 JSON files to a CSV of GPS data then plotting that data in R.

* [Massive Grep](https://github.com/nadir-it/parlorTricks/blob/main/massive_grep.sh)
<br/>
Massive_grep.sh was used to comb through approximately 250,000 JSON files worth of raw metadata and copy only the files with a GPS element.
This resulted in a directory filled with just under 70,000 files with GPS metadata in JSON format. Some of these had faulty or missing coordinates at this stage, but the script successfully removed nearly 80% of the files from the equation with a single command.

* [Scrape](https://github.com/nadir-it/parlorTricks/blob/main/scrape.py)
<br/>
Scrape.py was then used to extract as many useful coordinates as possible from these JSON files and store them in a CSV file. Where coordinates did not exist in the regular latitude and longitude fields, scrape.py checked a few backup possibilities before ultimately setting them to 0. They could have simply been discarded, however, these coordinates dropped safely in the Atlantic Ocean and as such would be filtered out by a single command in R as only United States data was being targeted. The CSV file contained 65,057 global entries.

* [Parlor Trick](https://github.com/nadir-it/parlorTricks/blob/main/parlorTrick.R)
<br/>
ParlorTrick.R imported and processed this data, then generated a point map of the United States and surrounding area. R was able to quickly filter out any remaining issues with the data resulting in 59,602 valid GPS coordinates in or near the United States. This script was made possible on a short notice by tidyverse and ggmap with map images provided by Stamen.

## Results
The end result of this project is so abstract as to effectively be no more than a generic population map of the United States. It does, however, demonstrate the scale of basic problems such as the lack of GPS metadata scrubbing on even a single social media website. In addition it demonstrates rapid application development and prototyping, data format conversions, and processing large file volumes.
