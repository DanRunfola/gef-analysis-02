
path <- "/vagrant/results/m2c"
dir.create(path)
file.remove(file.path(path, list.files(path)))

source("/home/vagrant/geoML/geoML.R")

full.dta <- read.csv("/vagrant/data_prep/analysis_cases/m2_data.csv",
                     check.names=FALSE, stringsAsFactors=FALSE)


# -----------------------------------------------------------------------------

#Calculate outcome
tot.forest.percent <- (full.dta$'00forest25.na.sum' -
                        rowSums(full.dta[33:46])) / full.dta$lossyr25.na.categorical_count


#Convert to square kilometers of forest cover
full.dta$tot.forest.km.outcome <- (as.vector(tot.forest.percent) * (pi * 10^2))

full.dta$chg.forest.km.outcome <- (rowSums(full.dta[33:45]) / (full.dta$lossyr25.na.categorical_count)) * (pi*10^2)

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
           "ltdr_yearly_ndvi_mean.2002.mean", "years_since_implementation"
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
              "NDVI (2002, Unitless)", "years_since_implementation"
)

out_path = "/vagrant/results/m2c/"

t <- geoML(dta=full.dta,
           trt=c("treatment", "Programmatic w/ Bio"),
           ctrl=c(Vars, VarNames),
           outcome=c("chg.forest.km.outcome", "2013 Forest Cover (Sq. km)"),
           out_path=out_path,
           file.prefix="FC_Hansen",
           kvar=c("v4composites_calibrated.2002.mean","dist_to_roads.na.mean",
                  "accessibility_map.na.mean","srtm_slope_500m.na.mean"),
           geog.fields = c("latitude", "longitude"),
           caliper=1.5,
           counterfactual.name = "Null Comparison",
           tree.ctrl = c(20,500),
           tree.cex = 0.25,
           col.invert = FALSE,
           tree.cnt = 100001
)



