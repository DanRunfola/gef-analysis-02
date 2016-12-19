#Extract relevant points from WDPA database
#To add to GEF Biodiversity geocoded dataset

#gef_id
#latitude
#longitude
library(maptools)
library(sp)

raw.path <- "/home/dan/Desktop/GitRepo/GEF_Programmatic/raw_data/other/WDPA/"

#Read in GEF lookups
GEF.WDPA.2014 <- read.csv(paste(raw.path, "IUCN GEF Project and PA Database 24Oct (2014).csv", sep=""), stringsAsFactors=FALSE)
GEF.WDPA.2015 <- read.csv(paste(raw.path, "PAsList (from Najeeb - 28 JUL 2015).csv", sep=""), stringsAsFactors=FALSE)

#Create empty holding vectors
gef_id <- ""
latitude <- ""
longitude <- ""
wdpa_id <- ""

for(i in 2:length(GEF.WDPA.2014[[1]]))
{
    wdpa_ids_it <- c(GEF.WDPA.2014$WDPA.ID[i],
                     GEF.WDPA.2014$X[i],
                     GEF.WDPA.2014$X.1[i],
                     GEF.WDPA.2014$X.2[i])
    for(j in 1:length(wdpa_ids_it))
    {
        gef_id <- c(gef_id, as.character(GEF.WDPA.2014$Project.ID[i]))
        wdpa_id <- c(wdpa_id, wdpa_ids_it[j])
    }
    

}

for(i in 1:length(GEF.WDPA.2015[[1]]))
{
    wdpa_ids_it <- c(GEF.WDPA.2015$WDPA.ID[i],
                     GEF.WDPA.2015$Other.WDPA.IDs[i])
    
    for(j in 1:length(wdpa_ids_it))
    {
        gef_id <- c(gef_id, as.character(GEF.WDPA.2015$Project..[i]))
        wdpa_id <- c(wdpa_id, wdpa_ids_it[j])
    }
}

WDPA.lookups <- data.frame(gef_id, wdpa_id, stringsAsFactors = FALSE)

#Get latitude and longitude for each WDPA site
WDPA.latlong <- read.csv(paste(raw.path, "WDPA_Dec2016-shapefile-points.csv", sep=""), stringsAsFactors=FALSE)

WDPA.lookups$lat <- ""
WDPA.lookups$lon <- ""

for(d in 2:length(WDPA.lookups[[1]]))
{
    if(WDPA.lookups$wdpa_id[d] != "")
    {
        if(summary(WDPA.latlong$WDPA_PID == WDPA.lookups$wdpa_id[d])[2][[1]] != "18800")
        {
        WDPA.lookups$lat[d] <- WDPA.latlong$XCOORD[WDPA.latlong$WDPA_PID == WDPA.lookups$wdpa_id[d]]
        WDPA.lookups$lon[d] <- WDPA.latlong$YCOORD[WDPA.latlong$WDPA_PID == WDPA.lookups$wdpa_id[d]]
        }
    }
}

write.csv(WDPA.lookups, paste(raw.path, "WDPA.latlongs.csv"))
