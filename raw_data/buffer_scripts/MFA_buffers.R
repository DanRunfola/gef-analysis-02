buffer.locations <- function(dta,
                              max.buffer=500000,
                              buffer.hole = 50000,
                              control.buffer = 10000,
                              control.cases = 5000,
                              out_t)
{
  set.seed(424)
  
  lonlat <- dta[,c("Longitude", "Latitude")]
  full.spdf <- SpatialPointsDataFrame(coords = lonlat, data = dta,
                                          proj4string = CRS("+proj=longlat +datum=WGS84 +ellps=WGS84"))
  
  #Create a buffered polygon from each area extending to
  #the outer buffer (max)
  #Then exclude all areas that fall within 20km of a project
  #Lambert Cylindrical Equal Area Transform
  full.spdf.trans <- spTransform(full.spdf, CRS("+proj=cea"))
  
  #Apply outer buffer
  buffers<-list()
  for(i in 1:nrow(full.spdf.trans)) {
    full.buffer <-disc(radius=max.buffer, centre=c(full.spdf.trans@coords[,1][i],full.spdf.trans@coords[,2][i]))
    discpoly<-Polygon(rbind(cbind(full.buffer$bdry[[1]]$x,
                                  y=full.buffer$bdry[[1]]$y), c(full.buffer$bdry[[1]]$x[1],
                                                               y=full.buffer$bdry[[1]]$y[1])))
    buffers<-c(buffers, discpoly)
  }
  
  spolys<-list()
  for(i in 1:length(buffers)) {
    spolybuff<-Polygons(list(buffers[[i]]), ID=row.names(dta)[i])
    spolys<-c(spolys, spolybuff)
  }
  
  full.buffers.spdf <-SpatialPolygons(spolys)
  
  #Create the treated unit polygons
  buffers<-list()
  for(i in 1:nrow(full.spdf.trans)) {
    full.buffer <-disc(radius=control.buffer, centre=c(full.spdf.trans@coords[,1][i],full.spdf.trans@coords[,2][i]))
    discpoly<-Polygon(rbind(cbind(full.buffer$bdry[[1]]$x,
                                  y=full.buffer$bdry[[1]]$y), c(full.buffer$bdry[[1]]$x[1],
                                                               y=full.buffer$bdry[[1]]$y[1])))
    buffers<-c(buffers, discpoly)
  }
  
  spolys<-list()
  for(i in 1:length(buffers)) {
    spolybuff<-Polygons(list(buffers[[i]]), ID=row.names(dta)[i])
    spolys<-c(spolys, spolybuff)
  }
  
  TREAT.buffers.spdf <-SpatialPolygons(spolys)
  
  
  
  #Apply buffer hole
  buffers<-list()
  for(i in 1:nrow(full.spdf.trans)) {
    full.buffer <-disc(radius=buffer.hole, centre=c(full.spdf.trans@coords[,1][i],full.spdf.trans@coords[,2][i]))
    discpoly<-Polygon(rbind(cbind(full.buffer$bdry[[1]]$x,
                                  y=full.buffer$bdry[[1]]$y), c(full.buffer$bdry[[1]]$x[1],
                                                               y=full.buffer$bdry[[1]]$y[1])))
    buffers<-c(buffers, discpoly)
  }
  
  spolys<-list()
  for(i in 1:length(buffers)) {
    spolybuff<-Polygons(list(buffers[[i]]), ID=row.names(dta)[i])
    spolys<-c(spolys, spolybuff)
  }
  
  full.buffers.exclusion.spdf <-SpatialPolygons(spolys)
  
  #Remove the exclusion zones from the outer buffers
  full.SampleZone.A = gDifference(full.buffers.spdf, full.buffers.exclusion.spdf)
  proj4string(full.SampleZone.A) <- CRS("+proj=cea")
  
  #Remove areas which do not fall within a continent (water)
  land.mask <- readOGR("data/countries.geojson", "OGRGeoJSON")
  
  land.mask.proj <- spTransform(land.mask, CRS("+proj=cea"))
  
  full.SampleZone = gIntersection(full.SampleZone.A, land.mask.proj)
  
  proj4string(full.SampleZone) <- CRS("+proj=cea")
  
  #Subsample within new buffers
  full.controls <- spsample(x=full.SampleZone@polyobj, n = control.cases, "stratified")
  
  #Buffer Control Cases
  buffers<-list()
  for(i in 1:length(full.controls)) {
    full.buffer <-disc(radius=control.buffer, centre=c(full.controls@coords[,1][i],full.controls@coords[,2][i]))
    discpoly<-Polygon(rbind(cbind(full.buffer$bdry[[1]]$x,
                                  y=full.buffer$bdry[[1]]$y), c(full.buffer$bdry[[1]]$x[1],
                                                               y=full.buffer$bdry[[1]]$y[1])))
    buffers<-c(buffers, discpoly)
  }
  
  spolys<-list()
  for(i in 1:length(buffers)) {
    spolybuff<-Polygons(list(buffers[[i]]), ID=row.names(full.controls)[i])
    spolys<-c(spolys, spolybuff)
  }
  
  full.controls <-SpatialPolygons(spolys)
  proj4string(full.controls) <- CRS("+proj=cea")
  
  full.controls.proj <- spTransform(full.controls, CRS("+proj=longlat +datum=WGS84 +ellps=WGS84"))
  
  proj4string(TREAT.buffers.spdf) <- CRS("+proj=cea")
  TREAT.buffers.proj <- spTransform(TREAT.buffers.spdf, CRS("+proj=longlat +datum=WGS84 +ellps=WGS84"))
  
  # Make spatial polygon data frame for export
  df<- data.frame(id = getSpPPolygonsIDSlots(full.controls.proj))
  row.names(df) <- getSpPPolygonsIDSlots(full.controls.proj)
  full.out <- SpatialPolygonsDataFrame(full.controls.proj, data =df)
  
  proj4string(full.out) <- CRS("+proj=longlat +datum=WGS84 +ellps=WGS84")
  
  df2<- data.frame(id = getSpPPolygonsIDSlots(TREAT.buffers.proj))
  row.names(df2) <- getSpPPolygonsIDSlots(TREAT.buffers.proj)
  TREAT.out <- SpatialPolygonsDataFrame(TREAT.buffers.proj, data =df2)

  proj4string(TREAT.out) <- CRS("+proj=longlat +datum=WGS84 +ellps=WGS84")
  
  #Save outputs
  writePolyShape(full.out, "/home/aiddata/Desktop/Github/GEF_MFA/generated_data/wb_controls.shp")
  
  writePolyShape(TREAT.out, out_t)
  
  write.csv(coordinates(full.out), "/home/aiddata/Desktop/Github/GEF_MFA/generated_data/control_centroids.csv")
  
  write.csv(coordinates(TREAT.out), "/home/aiddata/Desktop/Github/GEF_MFA/generated_data/treatment_centroids.csv")
  
}
