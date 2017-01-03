

source("~/geoValuate/geoValuate.R")


# bio3a, bio1a, and biom3b all use same dataset so we do not need to
# worry about merging to get data lined up - can just pull columns out of dataframe

NDVI.dta <- read.csv("/vagrant/results/bio3a/Biodiversity_prediction.csv",
                     check.names = FALSE,
                     stringsAsFactors=FALSE)

state.dta <- read.csv("/vagrant/results/bio1a/Biodiversity_prediction.csv",
                      check.names = FALSE,
                      stringsAsFactors=FALSE)

fc.dta <- read.csv("/vagrant/results/biom3b/forest_cover_prediction.csv",
                   check.names = FALSE,
                   stringsAsFactors = FALSE)


# need raw data to get IBA area for bio valuation
#   this must be merged with one of the above dataframes since it
#   is the original dataset and does not line up with the above data
base.dta <- read.csv("/vagrant/data_prep/analysis_cases/base_data.csv",
                     check.names = FALSE,
                     stringsAsFactors = FALSE)

# GEF ID is not unique, so use coords to make new str field which can be used
# as index to get IBA area information
state.dta$coord_str <- paste(state.dta$longitude, state.dta$latitude, sep='_')
base.dta$coord_str <- paste(base.dta$longitude, base.dta$latitude, sep='_')


get_iba_area <- function(coord_str) {
  tmp_vals <- base.dta[which(base.dta$coord_str == coord_str), ]
  # print(tmp_vals[1, 'iba_area'])
  return(tmp_vals[1, 'iba_area'])
}

state.dta$iba_area <- apply(state.dta, 1, function(z) get_iba_area(z['coord_str']))



# -----------------------------------------------------------------------------

outpath <- "/vagrant/results/biom2c/"


geoValuate.bio.soilRetention(
  NDVI.dta$ltdr_yearly_ndvi_mean.2002.mean,
	NDVI.dta$tree.pred,
  outpath)

geoValuate.bio.recreation(
  state.dta$tree.pred,
  state.dta$iba_area,
  outpath)

geoValuate.carbon(
  NDVI.dta$tree.pred,
  fc.dta$tree.pred,
  NDVI.dta$srtm_slope_500m.na.mean,
  NDVI.dta$udel_air_temp_v4_01_yearly_mean.2002.mean,
  outpath)
