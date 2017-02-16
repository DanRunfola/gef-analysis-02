# generating 10km buffer for GEF LD
#Libraries
library(sp)
library(rgdal)
library(spatstat)
library(maptools)
library(rgeos)
library(geojsonio)
library(MatchIt)
library(rpart)
library(Rcpp)
library(doBy)
sourceCpp("/home/aiddata/Desktop/Github/GEF_MFA/Analyses/split.cpp")

#Functions
source("/home/aiddata/Desktop/Github/GEF_MFA/data_processing/MFA_data_functions.R")
source("/home/aiddata/Desktop/Github/GEF_MFA/data_processing/MFA_buffers.R")
source("/home/aiddata/Desktop/Github/GEF_MFA/data/gef_ld_locations.tsv")
#source("/home/aiddata/Desktop/Github/GEF_MFA/Analyses/CT_ForestCover.R")
#source("/home/aiddata/Desktop/Github/GEF_MFA/Analyses/CT_NDVI.R")
#source("/home/aiddata/Desktop/Github/GEF_MFA/Analyses/causal_tree_functions.R")
#source("/home/aiddata/Desktop/Github/GEF_MFA/Analyses/descriptives.R")

ld.locations <- read.csv(file ="/home/aiddata/Desktop/Github/GEF_MFA/data/gef_ld_locations.tsv", sep = '\t')

buffer.locations(dta=ld.locations,
                 max.buffer=500000,
                 buffer.hole = 50000,
                 control.buffer = 10000,
                 control.cases = 5000,
                 out_t = "/home/aiddata/Desktop/Github/GEF_MFA/generated_data/ld_treatment_10buffer.shp")


