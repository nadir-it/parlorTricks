library(tidyverse)
library(ggmap)

#setwd("C:/Users/name/Desktop")
#select columns to load from CSV
datavars <- c("filetag","latitude","longitude", "elevation", "creation_date", 
              "creation_time", "modified_date", "modified_time")
#load csv file
videos <- read.csv("data/clean_data.csv", header = TRUE)[,datavars]
#isolate column headers we need, redundant step in this case.
data <- select(videos, longitude, latitude, filetag)
#safety check for bad data points
data = na.omit(object = data)
#isolate the American Continent
americans <- data %>%
  filter(
    -125 < longitude & longitude < -67,
    23.75 < latitude & latitude < 49
  )
#use map frame
us <- c(left = -125, bottom = 23.75, right = -67, top=49)
#pull map data from stamen
map <- get_stamenmap(us, zoom=5, maptype = "toner-lite")
#data point position and coloring
dots <- geom_point(data = americans,
                   aes(x = longitude, y = latitude),
                   alpha = 0.1,
                   colour = "orange",
                   fill = "black")
#create labeling for map
title <- labs(title = "GPS Metadata of Parler Videos",
              x = "Longitude",
              y = "Latitude")
#generate plotable map package
mymap <- ggmap(map) + dots + title
plot(mymap)
