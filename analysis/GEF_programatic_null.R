source("/Users/Zhonghui/Documents/AidData/REU/github/geoML/geoML.R")

full.dta <- read.csv("/Users/Zhonghui/Documents/AidData/REU/github/GEF_Programmatic/data_prep/merged_data.csv")
full.dta.gef <- read.csv('/Users/Zhonghui/Documents/AidData/REU/github/GEF_Programmatic/raw_data/gef_projects_160726.csv')
full.mfa.dta <- read.csv("/Users/Zhonghui/Documents/AidData/REU/github/GEF_Programmatic/raw_data/other/mfa_export.csv")
#prog.control <- read.csv("/Users/Zhonghui/Documents/AidData/REU/github/GEF_Programmatic/raw_data/programmatic_control.csv")


prog.control <- full.dta[full.dta$type=='rand',]
prog.control$treatment <- 0


#dta.cd.mfa <- read.csv('/Users/Zhonghui/Documents/AidData/REU/github/GEF_Programmatic/raw_data/CD_MFA_CD_projects_sheet.csv')
#dta.mfa.mfa <- read.csv('/Users/Zhonghui/Documents/AidData/REU/github/GEF_Programmatic/raw_data/CD_MFA_MFA_projects_sheet.csv')

#dta.mfa.cd.mfa.mfa.merge <- merge(dta.mfa.mfa, dta.cd.mfa, by.x="GEF.ID", by.y="GEF.ID")



# create treatment and contral data
programatic.dta <- full.dta[ which(full.dta$type=='prog'), ] #which(full.dta$type=='prog'& full.dta$treatment ==1)
#ld.dta <- full.dta[ which(full.dta$type=='land'), ]


programatic.dta.fullgef <- merge(programatic.dta, full.dta.gef, by.x="gef_id", by.y="GEF_ID")

ld.prog.full <- programatic.dta.fullgef[programatic.dta.fullgef$Focal.Area=='Land Degradation',]
programatic.dta.ld.mfa <- programatic.dta.fullgef[programatic.dta.fullgef$gef_id %in% full.mfa.dta$gef_id, ]

ld.prog.all <- rbind(programatic.dta.ld.mfa, ld.prog.full)
ld.prog.all$treatment <- 1




ld.merge <- ld.prog.all[,names(ld.prog.all) %in% names(prog.control)]
mfa.merge <- prog.control[,names(prog.control) %in% names(ld.merge)]

final <- rbind(ld.merge, mfa.merge)
write.table(final, file = "/Users/Zhonghui/Documents/AidData/REU/github/GEF_Programmatic/data_prep/ld.prog.control.all.csv",row.names=FALSE, na="", col.names=TRUE, sep=",")



#programatic.dta.ld <- programatic.dta[programatic.dta$gef_id %in% ld.dta$gef_id, ]

programatic.dta.fullgef <- merge(programatic.dta, full.dta.gef, by.x="gef_id", by.y="GEF_ID")
dta.1 <- merge(programatic.dta, full.dta.gef, by.x="gef_id", by.y="GEF_ID")









#==================================================================================
#==================================================================================
#Summarizing Financials and timestamps (this should be done in the data prep scripts
#in the future).
total <- as.numeric(gsub(",","",as.character(full.dta$Cofinance.CEO.endorse.stage))) +  
  as.numeric(gsub(",","",as.character(full.dta$GEF.Project.Grant.CEO.endorse.stage)))
cofinancing <- as.numeric(gsub(",","",as.character(full.dta$Cofinance.CEO.endorse.stage))) / total
full.dta$cofinance.ratio <- cofinancing 
full.dta$total.funding <- total
full.dta$GEF.funding <- as.numeric(gsub(",","",as.character(full.dta$GEF.Project.Grant.CEO.endorse.stage)))
full.dta$cofinance.funding <- as.numeric(gsub(",","",as.character(full.dta$Cofinance.CEO.endorse.stage)))

# remove NA data
full.dta <- full.dta[!is.na(full.dta$Actual.date.of.implementation.start),]
full.dta <- full.dta[!(as.character(full.dta$Actual.date.of.implementation.start) == ""),]
full.dta$start.date <- as.Date(full.dta$Actual.date.of.implementation.start, format="%d-%b-%y")
full.dta$year <- as.numeric( format( full.dta$start.date, '%Y'))
full.dta$wdpa_5km.na.sum <- full.dta$wdpa_5km.na.sum / 4

#Calculate outcome
#?????????????????????????????????????????? Percentage of forsest????????? ZLV
tot.forest.percent <- (full.dta$X00forest25.na.sum - 
                         (rowSums(full.dta[336:350])-full.dta[341])) / full.dta$lossyr25.na.categorical_count

#Convert to square kilometers of forest cover 
#???????????????????Is this assume the radius is 10 Unit??? ZLV
full.dta$tot.forest.km.outcome <- as.vector(tot.forest.percent)[[1]] * (pi * 10^2)
#==================================================================================
#==================================================================================
#Define control variables
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
           "Region",  "GEF.replenishment.phase",
           "cofinance.ratio", "total.funding", "GEF.funding")

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
              "NDVI (2002, Unitless)", "Region", "Replenishment Phase",
              "Cofinance Ratio (% Total)", "Total Funding", "GEF funding"
)

out_path = "/home/aiddata/Desktop/Github/geoML/GEF_MFA/LD_MFA_Contrast/FC/"

t <- geoML(dta=full.dta, 
           trt=c("treatment", "GEF MFA Projects"), 
           ctrl=c(Vars, VarNames), 
           outcome=c("tot.forest.km.outcome", "2013 Forest Cover (Sq. km)"), 
           pth=out_path, 
           file.prefix="FC_Hansen", 
           kvar=c("GEF.funding","cofinance.ratio",
                  "treecover2000.na.mean","total.funding"),
           geog.fields = c("latitude", "longitude"),
           caliper=1.0,
           counterfactual.name = "Land Degradation",
           tree.ctrl = c(20,20),
           col.invert = FALSE,
           tree.cnt = 10000
)
