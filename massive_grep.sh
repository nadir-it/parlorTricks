#!/usr/bin/env bash
#copy every JSON file with GPS metadata

for filename in ./metadata/*.json; do
	grep -l "GPS"  $filename | xargs -r cp -t ./gps_data/ &;
done
