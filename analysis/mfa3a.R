
path <- "/vagrant/results/mfa3a"
dir.create(path)
file.remove(file.path(path, list.files(path)))

source("/home/vagrant/geoML/geoML.R")

full.dta <- read.csv("/vagrant/data_prep/analysis_cases/mm3_data.csv", check.names = FALSE)
#/vagrant/data_prep/analysis_cases/m3_data.csv


# -----------------------------------------------------------------------------


full.dta$'GEF Project Grant CEO endorse stage' <- gsub(",","",full.dta$'GEF Project Grant CEO endorse stage')
full.dta$'GEF Project Grant CEO endorse stage' <- as.numeric(as.character(full.dta$'GEF Project Grant CEO endorse stage'))

full.dta$'Cofinance CEO endorse stage' <- gsub(",","",full.dta$'Cofinance CEO endorse stage')
full.dta$'Cofinance CEO endorse stage' <- as.numeric(as.character(full.dta$'Cofinance CEO endorse stage'))

full.dta <- full.dta[!is.na(full.dta$'GEF Project Grant CEO endorse stage'),]


# -----------------------------------------------------------------------------


# Define control variables
Vars <-  c("dist_to_all_rivers.na.mean", "dist_to_roads.na.mean",
           "srtm_elevation_500m.na.mean", "srtm_slope_500m.na.mean",
           "accessibility_map.na.mean", "gpw_v3_density.2000.mean",
           "wdpa_5km.na.sum", "treecover2000.na.mean", "latitude",
           "longitude", "udel_precip_v4_01_yearly_max.2002.mean",
           "udel_precip_v4_01_yearly_min.2002.mean",
           "udel_precip_v4_01_yearly_mean.2002.mean",
           "udel_air_temp_v4_01_yearly_max.2002.mean",
           "udel_air_temp_v4_01_yearly_min.2002.mean",
           "udel_air_temp_v4_01_yearly_mean.2002.mean",
           "v4composites_calibrated.2002.mean",
           "ltdr_yearly_ndvi_mean.2002.mean", "GEF.Project.Grant.CEO.endorse.stage",
           "iba_distance"
)

VarNames <- c("Dist. to Rivers (m)", "Dist. to Roads (m)",
              "Elevation (m)", "Slope (degrees)",
              "Urb. Dist. (rel)", "Pop. Density (2000)",
              "Protected Area %", "Treecover (2000, %)", "Latitude",
              "Longitude", "Max Precip. (2002, mm)",
              "Min Precip (2002, mm)",
              "Mean Precip (2002, mm)",
              "Max Temp (2002, C)",
              "Min Temp (2002, C)",
              "Mean Temp (2002, C)",
              "Nightime Lights (2002, Relative)",
              "NDVI (2002, Unitless)", "GEF Funding",
              "Distance to IBA"
)

out_path = "/vagrant/results/mfa3a/"

t <- geoML(dta=full.dta,
           trt=c("treatment", "Programmatic multi-country w/ Bio"),
           ctrl=c(Vars, VarNames),
           outcome=c("iba_statescore", "IBA State Score"),
           out_path=out_path,
           file.prefix="IBA_state",
           kvar=c("v4composites_calibrated.2002.mean","dist_to_roads.na.mean",
                  "accessibility_map.na.mean","srtm_slope_500m.na.mean"),
           geog.fields = c("latitude", "longitude"),
           caliper=1.5,
           counterfactual.name = "Non-programmatic single-country w/ Bio",
           tree.ctrl = c(2,10),
           col.invert = FALSE,
           tree.cnt = 100001
)
