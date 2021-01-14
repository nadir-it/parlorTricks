#!/usr/bin/env python3
import json
import os
import csv
import re
import string


def formatElev(elev):
    """ Format elevation from metadata """

    e = elev.split(' ')
    return e[0]

#split date time info 2020:11:15 04:10:26
def splitDateTime(dt):
    """Format date time from metadata """

    dt = dt.split(' ')
    date = str(dt[0])
    time = dt[1]
    dateDict = date.maketrans(":","/")
    date = date.translate(dateDict)
    return date, time

#52 deg 30' 36.00" N
def convertLatLongToGoogleMapsCoord(latlong):
    """ Convert GPS dms metadata to Google Maps compatible DD """

    intermediate = latlong.split(' ')
    if intermediate[0] == '':
        intermediate[0] = 0

    try:
        sec = intermediate[3]
    except IndexError:
        sec = '0'
    try:
        mins = intermediate[2]
    except IndexError:
        mins = '0'
    try:
        direct = intermediate[4]
    except IndexError:
        direct = "X"

    dmsBuffer = {
        "degrees": float(intermediate[0]),
        "minutes": float(mins.strip(string.punctuation))/60,
        "seconds": float(sec.strip(string.punctuation))/(60*60),
        "direction": direct,
    }

    ddBuffer = dmsBuffer["degrees"] + dmsBuffer["minutes"] + dmsBuffer["seconds"]
    if dmsBuffer["direction"] == 'W' or dmsBuffer["direction"] == 'S':
        ddBuffer *= -1 
    return "{:.6f}".format(ddBuffer)

# "38 deg 54' 38.88\" N, 94 deg 40' 8.04\" W"
def splitGPSPos(gpspos):
    """ Split GPSPosition in last desperate attempt to get GoogleAPI compatible coordinates """
    latlong = gpspos.split(',')
    latlongDict = latlong.maketrans("/", "")
    latlong = latlong.translate(latlongDict)
    lat = latlong[0]
    long = latlong[1]
    return lat, long

def getJSONAttributes(name, JSONchunk):
    """Try to get GPS data from JSON"""

    #get media creation date
    try:
        mediaCreatedDate = JSONchunk["MediaCreateDate"]
    except KeyError:
        mediaCreatedDate = "2001:01:01 01:01:01"
    #get media modified date
    try:
        mediaModifyDate = JSONchunk["MediaModifyDate"]
    except KeyError:
        mediaModifyDate = "2001:01:01 01:01:01"
    #get latitude
    try:
        gpsLatitude = JSONchunk["GPSLatitude"]
    except KeyError:
        gpsLatitude = "00 deg 00' 00.00\" S"
    #get longitude
    try:
        gpsLongitude = JSONchunk["GPSLongitude"]
    except KeyError:
        gpsLongitude = "00 deg 00' 00.00\" W"
    #get elevation
    try:
        gpsElevation = JSONchunk["GPSAltitude"]
    except KeyError:
        gpsElevation = "0.00 m"
    #get model
    try:
        model = JSONchunk["Model"]
    except KeyError:
        model = "UNKNOWN"

    if gpsLatitude == "00 deg 00' 00.00\" S":
        try:
            gpsLatitude = JSONchunk["PantryGPSLatitude"]
        except:
            gpsLatitude = "00 deg 00' 00.00\" S"
    
    if gpsLongitude == "00 deg 00' 00.00\" W":
        try:
            gpsLongitude = JSONchunk["PantryGPSLongitude"]
        except:
            gpsLongitude = "00 deg 00' 00.00\" W"

    if gpsLatitude == "00 deg 00' 00.00\" S" and gpsLongitude == "00 deg 00' 00.00\" W":
        try:
           gpsLatitude, gpsLongitude = splitGPSPos(JSONchunk["GPSPosition"])
        except:
            gpsLatitude = "00 deg 00' 00.00\" S"
            gpsLongitude = "00 deg 00' 00.00\" W"

    
    gpsLatitude = convertLatLongToGoogleMapsCoord(gpsLatitude)
    gpsLongitude = convertLatLongToGoogleMapsCoord(gpsLongitude)

    cDate, cTime = splitDateTime(mediaCreatedDate)
    mDate, mTime = splitDateTime(mediaModifyDate)
    altitude = formatElev(gpsElevation)
    caught = name + "," + gpsLatitude + "," + gpsLongitude + "," + altitude + "," + cDate + "," + cTime + "," + mDate + "," + mTime + "," + model
    return caught

def getTag(p):
    #print(p)
    filename = os.path.basename(p)
    splitname = os.path.splitext(filename)
    basename = splitname[0]
    splitbase = basename.split('-')
    tag = splitbase[1]
    #print(tag)
    return tag

def main():
    #folder with gps tagged JSON files
    directory = './gps_data/'

    #with open('data.csv', 'a') as outputfile:
    outputfile = open('data.csv', 'w')
    fileHeader = 'filetag,latitude,longitude,elevation,creation_date,creation_time,modified_date,modified_time,phone_model'
    outputfile.write( fileHeader +'\n')

    count = 0
    print(fileHeader)
    for file in os.listdir(directory):
    #complete path for python
        #if count > 1000:
            #break
        path = directory + file
        t = getTag(path)
        json_file = open(path, 'r')
        buffer = json_file.read()
        data = json.loads(buffer)
    
        #python why you do this to me?
        passthru = data[0]
    
        #finally start actuall getting the json data
        caught = getJSONAttributes(t,passthru)

        #print(caught)
        outputfile.write(caught + '\n')

        json_file.close()
        print(count)
        count = count + 1
    
    outputfile.close()

if __name__ == "__main__":
    main()



