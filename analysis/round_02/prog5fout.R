

case <- "prog5fout"

path <- paste("/vagrant/results/", case, '/', sep="")
dir.create(path)
file.remove(file.path(path, list.files(path)))

source("/home/vagrant/geoML/geoML.R")

input <-paste("/vagrant/data_prep/analysis_cases/", case, "_data.csv", sep="")
full.dta <- read.csv(input, check.names=FALSE, stringsAsFactors=FALSE)


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
           "ltdr_yearly_ndvi_mean.2002.mean",
           "years_since_implementation",
           # "total_commitments",
           # "gef_phase_3",
           # "gef_phase_4", "gef_phase_5"#,
           # "gef_phase_6", "gef_phase_other"
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
              "NDVI (2002, Unitless)",
              "years since implementation",
              # "total commitments",
              # "gef phase 3",
              # "gef phase 4", "gef phase 5"#,
              # "gef phase 6", "gef phase other"
)


t <- geoML(dta=full.dta,
           trt=c("treatment", "Programmatic MFA Land with Monetary Threshold"),
           ctrl=c(Vars, VarNames),
           outcome=c("chg.forest.km.outcome", "2013 Forest Cover (Sq. km)"),
           out_path=path,
           file.prefix="FC_Hansen",
           kvar=c("v4composites_calibrated.2002.mean","dist_to_roads.na.mean",
                  "accessibility_map.na.mean","srtm_slope_500m.na.mean"),
           geog.fields = c("latitude", "longitude"),
           caliper=0.5,
           counterfactual.name = "Non-Programmatic MFA Land with Monetary Threshold",
           tree.ctrl = c(5,500),
           tree.cex = 0.25,
           col.invert = TRUE,
           tree.cnt = 100001
)
