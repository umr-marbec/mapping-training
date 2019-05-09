###########################################################
# Mapping Lake Togo artisanal fisheries landing Positions
###########################################################
# Needed : 
# csv datafile togo.csv
# libraries sp, sf, tmap, tmaptools, openstreetmap
###########################################################
rm(list=ls())

togo <- read.csv("togo.csv", 
                header = TRUE, sep=";", dec=".")
togo$Agglomération <- as.character(togo$Agglomération)
togo$Secteur <- as.integer(togo$Secteur)

# Just to check :
# # Plot the spatial position of the sites using the xyplot function from package lattice
library(lattice)
xyplot(Latitude  ~ Longitude,
       aspect = "iso",
       col = 1,
       xlab = "X coordinate",
       ylab = "Y coordinate",
       data = togo,
       pch = 16)

with(togo,range(Longitude))
with(togo,range(Latitude))

# From the range above, define the "lactogo" area for maps
lactogo<- c(1.35,6.18,1.66,6.34)


##############################################################
#Next we will plot the spatial coordinates using ggmap package
#You need to have internet access to run this block of code.

# Converts the coordinates to WGS84 (package sp)
library(sp)
togo.spdf <- togo 
coordinates(togo.spdf) <- ~Longitude + Latitude

# this gets the proper proj parameters
WGS84 <- CRS("+proj=longlat +datum=WGS84")
projtogo <- CRS("+init=epsg:4326")
proj4string(togo.spdf) <- projtogo

# this reprojects the file from togo to wgs84
togo_wgs84.spdf <- spTransform(togo.spdf,WGS84)


# Get the map using ggmap package and Stamen

# We add these to the togo dataframe
togo$Longitude2    <- togo_wgs84.spdf$Longitude
togo$Latitude2    <- togo_wgs84.spdf$Latitude

range(togo$Longitude2)
range(togo$Latitude2)
# Here, same as original latitude and longitude, but sometimes not

library(ggplot2)
library(ggmap)
glgmap   <- get_map(location = lactogo,
                    source= "stamen",
                    maptype= "terrain",
                    col = "color")

# Then plot the map 
p <- ggmap(glgmap)
p

# Add only the points and tickmarks as decimal degrees
p <- p + geom_point(aes(Longitude2, Latitude2),
                    data = togo,
                    size = 2)
p <- p + xlab("Longitude") + ylab("Latitude")
p <- p + theme(text = element_text(size = 10))
p

# Change the lat/lon plotting to degrees/minutes (manual transformation...)
p <- p + scale_x_continuous (breaks= c(1.4167,1.5,1.5834),label = c("1°25E","1°30E","1°35E"), 
                             expand = expand_scale(mult=0, add = 0))
p <- p + scale_y_continuous (breaks= c(6.167,6.25,6.334),label = c("6°10N","6°15N","6°20N"), 
                             expand = expand_scale(mult=0, add = 0))
p

# Add a square line around the map
p <- p + theme(text = element_text(size = 12), 
               panel.border = element_rect(linetype = 1, fill=NA))
p

# Remove axes labels
p <- p + xlab("") + ylab("")
p

# Add points names
p <- p + geom_text(aes(x = Longitude2, y = Latitude2, label = Agglomération, fontface="bold"), 
                   data = togo, 
                   size = 4, 
                   vjust = 0, 
                   hjust =-0.15)
p

# When the graph is perfect, you can save it directly into a JPEG file :
jpeg(filename="MapTogoLake_ggmap.jpg", height=450, width=650)
p
dev.off()



# Same plot using library tmap ################################
library(tmap)

# maps can be done either in view mode (interactive) or plot mode (for printing)

# View mode (interactive) ##############
tmap_mode("view")

#tm_basemap(leaflet::providers$Esri.OceanBasemap) +  
tm_basemap(leaflet::providers$Esri.WorldImagery) +
tm_shape(togo_wgs84.spdf, bbox = lactogo) +
tm_bubbles(col = "white", size=0.5, group="Lake Togo landing sites") +
tm_text("Agglomération", col="white", size=1.5, just="bottom", ymod=0)


# Plot mode ##########################
library(sf)
library(tmaptools)

tmap_mode("plot")

# Define the zone to plot
zone <- st_bbox(c(xmin=1.35, xmax=1.66, ymax= 6.34, ymin=6.18), crs=st_crs(4326)) # from sf

# Get basemap of this zone using read_osm()
# type can be predefined (e.g. 'esri' or 'bing'...)
# or can be defined using the server adress
# Choose one of the followings :

# osm_zone <- read_osm(x=zone, current.projection='CRS', type='esri') # from tmaptools
osm_zone <- read_osm(x=zone, current.projection='CRS', type='bing') # from tmaptools
# osm_zone <- read_osm(x=zone, current.projection='CRS', type=paste0("https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/",
#         "MapServer/tile/{z}/{y}/{x}'"))
# osm_zone <- read_osm(x=zone, current.projection='CRS', type='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')

# Quick view of the basemap before plotting
qtm(osm_zone)

# replace the tm_basemap() instruction by a tm_shape() to load osm_zone plus a tm_raster()
tm_shape(osm_zone) +
tm_raster() +
tm_shape(togo_wgs84.spdf, bbox = lactogo) +
tm_symbols(col = "white", group="Lake Togo landing sites", size="Landings", shape=16)+
tm_text("Agglomération", size=1.5, col="white", just="bottom", ymod=1) +
tm_legend(legend.text.color="white", frame=T , bg.color="darkgrey")

# shape parameter for tm_symbols() : 15=square ; 16=round ; 17=triangle ; 18=diamond ...


# When the graph is perfect, you can save it directly into a JPEG file :
jpeg(filename="MapTogoLake_tmap.jpg", height=450, width=650)
tm_shape(osm_zone) +
  tm_raster() +
  tm_shape(togo_wgs84.spdf, bbox = lactogo) +
  tm_symbols(col = "white", group="Lake Togo landing sites", size="Landings", shape=16)+
  tm_text("Agglomération", size=1.5, col="white", just="bottom", ymod=1) +
  tm_legend(legend.text.color="white", frame=T ,bg.color="darkgrey")
dev.off()



