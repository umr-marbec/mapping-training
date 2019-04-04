import Nio, Ngl
import numpy as np
import shapefile as pyshp
from glob import glob

flist = glob("script_connectivity_output/nicolas/points_all.shp")

def read_shape(f):

    outdic = {}

    tocorr = False

    fin = pyshp.Reader(f)
    shapes = fin.shapes()
    records = fin.records()
    fields = fin.fields

    fields = np.array([s[0] for s in fields])
    fields = fields[1:]

    # checks that the shapefile contains the long/latg attribute.
    # if so, data from shapefile will be corrected
    #if 'long' in fields:
    if 'Longitude' in fields:
        tocorr = True
        ilon = np.nonzero(fields=='Longitude')[0][0]
        ilat = np.nonzero(fields=='Latitude')[0][0]

    nshapes = len(shapes)
    
    # loop over all the shapes from the shapefile
    for ishape in xrange(0, nshapes):

        # extracts the shape name
        name = records[ishape][0]
        # The SA file has no name record. We hence force it.0
        if str(name) == '30.0':
            name = 'SA' 
        
        # extract shape points
        points = shapes[ishape].points

        # converts into lon/lat and stores in the dict
        lon = np.array([s[0] for s in points])
        lat = np.array([s[1] for s in points])

        outdic[name] = {'lat': lat, 'lon':lon}

    return outdic


################################################################################ list of labels to draw
off = 0.7
dictlabels = {}
dictlabels['Madagascar'] = {'lon': 45.2 + 1.4, 'lat':-20, 'rotation':0, 'color':'black', 'fontsize':10, 'weight':'bold'}
dictlabels['Un-named Seamount'] = {'lat': -31.14055556 + 0.5, 'lon':  42.84027778, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Atlantis Bank'] = {'lat': -32.21916667+1, 'lon':  57.28583333+3, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Sapmer Bank'] = {'lat': -36.3+0.6, 'lon':  52.12555556, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Middle of What Seamount'] = {'lat': -37.46777778-1, 'lon':  50.41861111+8, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Walters Shoal'] =  {'lat': -32.54085278 - 1.5, 'lon': 43.76924167, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Coral Seamount'] = {'lat': -40.90583333-1.5, 'lon': 42.85916667, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Melville Bank'] = {'lat': -38.97805556-0.5, 'lon': 46.75138889-3.5, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['South Africa'] = {'lat': -31.5, 'lon': 25.5-1+0.5, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'bold'}
dictlabels['Mozambique'] = {'lat': -15, 'lon': 38, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'bold'}
dictlabels['Indian Ocean'] = {'lat': -10, 'lon': 60 + 15/2., 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'bold'}
dictlabels['Tofo'] = {'lat': -23.999755192878336+ off+0.5, 'lon': 36, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Fort Dauphin'] = {'lat': -25.999755192878336 + off-0.8, 'lon': 47.0 + 5, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Tulear'] = {'lat': -23.659755192878336 - off, 'lon': 43., 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Mamanjary'] = {'lat': -21.999755192878336 + off -1.5 , 'lon': 48.9, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['La Reunion'] = {'lat':-21.079755192878338 - 1+0.5, 'lon': 55.120000000000005+4.3, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'bold'}
dictlabels['Maurice'] = {'lat': -20.37975519287834 - 1+1.1, 'lon':57.1 +4.4 , 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'bold'}
dictlabels['La Perouse'] = {'lat': -19.71975519287834 + off+0.5, 'lon': 54.17, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Sainte Marie'] = {'lat': -16.96975519287834 + off, 'lon': 50.4, 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Santa Lucia'] = {'lat': -28.59975519287834 - off+1.5, 'lon': 32.6 , 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}
dictlabels['Mad-ridge'] = {'lat':-27.499755192878336 - off-0.3, 'lon':46.25 , 'rotation':0, 'color':'black', 'fontsize':6, 'weight':'unbold'}

######################################################## reading topo
fin = Nio.open_file('sub_ETOPO1_Bed_g_gmt4.grd')
lonb = fin.variables['x'][:]
latb = fin.variables['y'][:]
bathy = fin.variables['z'][:]
bathy = bathy * 1e-3    # conversion to km
bathy = np.ma.masked_where(bathy>0, bathy)
fin.close()
####################################################### end reading topo


######################################################## reading current velocities
fin = Nio.open_file('oscar_vel.nc', 'r')

itime = 0
    
lon = fin.variables['longitude'][:]
lat = fin.variables['latitude'][:]

lon, lat = np.meshgrid(lon, lat)

u = fin.variables['u'][itime, 0, :, :]
v = fin.variables['v'][itime, 0, :, :]

fin.close()

u = np.ma.masked_where(np.isnan(u), u)
v = np.ma.masked_where(np.isnan(v), v)
speed = np.sqrt(u*u + v*v)

speed *= 100
u *= 100
v *= 100

############################################ end of velocity processing

# init workspace
resngl = Ngl.Resources()
colors = ['White', 'Black']
resngl.wkColorMap = "gsltod"
wks = Ngl.open_wks("png", "oscar_traj_%s" %'mean', resngl)

# add color to colomap
cgray = 3*[0.7]
Ngl.new_color(wks, cgray[0], cgray[1], cgray[2])

with open('colors.txt', 'r') as fin:
    lines = fin.readlines()
    for l in lines:
        temp = np.array(l.split()).astype(np.float)
        Ngl.new_color(wks, temp[0], temp[1], temp[2])


################################## setting the resources for the bathymetry contour map
res = Ngl.Resources()

res.nglDraw = False
res.nglFrame = False
# Set map resources.
res.mpLimitMode = "LatLon"     # limit map via lat/lon
res.mpMinLatF = -45         # map area
res.mpMaxLatF = -5    # latitudes
res.mpMinLonF = 20     # and
res.mpMaxLonF = 81     # longitudes
res.mpFillOn = True
res.mpLandFillColor = "LightGray"
res.mpOceanFillColor = -1
res.mpInlandWaterFillColor = "LightBlue"
res.mpGeophysicalLineThicknessF = 1.5
res.mpOutlineOn   = True
res.mpGridAndLimbOn = False
res.mpOutlineBoundarySets = "National"
res.mpFillOn                    = True

res.lbLabelStride = 4
res.lbOrientation = "Vertical" # vertical colorbar 
res.lbTitleString = "Bathymetry (km)" # cbar title string
res.lbTitlePosition = "Right" # cbar title position
res.lbTitleAngleF = 90 
res.lbTitleDirection = "Across"
res.lbTitleFontHeightF = 0.01
res.lbLabelFontHeightF = 0.01

# Scalar field resources
res.sfXArray        = lonb
res.sfYArray        = latb

res.cnFillOn                    = True
res.cnLinesOn                   = False
res.cnLineLabelsOn              = False
res.cnFillMode = "CellFill"
res.nglSpreadColorEnd = 2 # index of first color for contourf 
res.nglSpreadColorStart = 27 # index of last color for contourf
res.cnLevelSelectionMode="ExplicitLevels"
res.cnLevels = np.arange(-8, 0+0.25, 0.25)
res.pmLabelBarWidthF = 0.06 # cbar width 

# map tick managements
res.tmYROn       = True
res.tmYRLabelsOn = False
res.tmYLOn       = True
res.tmYLLabelsOn = True

res.tmXTOn       = True
res.tmXTLabelsOn = True
res.tmXBOn       = True
res.tmXBLabelsOn = True


contour = Ngl.contour_map(wks, bathy, res)



resvec = Ngl.Resources()
resvec.vcRefMagnitudeF  = 20.
resvec.vcRefLengthF     = 0.02
resvec.vcMinDistanceF = 0.01
resvec.vcGlyphStyle = 'CurlyVector'
resvec.vcMonoLineArrowColor  = False  # Draw vectors in colors 
resvec.vcRefAnnoOn = False # no reference arrow

# settings for the colorbar
resvec.lbOrientation = "Horizontal" # vertical colorbar 
resvec.lbTitleString = "Current speed (cm/s)" # cbar title string
resvec.lbLabelFontHeightF = 0.01
resvec.lbTitleFontHeightF = 0.01
resvec.lbTitlePosition = 'Bottom'
resvec.lbLabelOffsetF = 0.2
resvec.lbTitleOffsetF = 0.2
resvec.lbLabelStride = 2

resvec.nglSpreadColorEnd = 34 # index of first color for contourf 
resvec.nglSpreadColorStart = 133 # index of last color for contourf
resvec.nglSpreadColorStart, resvec.nglSpreadColorEnd = resvec.nglSpreadColorEnd, resvec.nglSpreadColorStart
resvec.nglDraw = False
resvec.nglFrame = False

resvec.vfXArray = lon
resvec.vfYArray = lat
resvec.vcLevelSelectionMode="ExplicitLevels"
resvec.vcLevels = np.arange(0, 50 + 2.5, 2.5)
resvec.vcLineArrowThicknessF      = 2

resvec.pmLabelBarHeightF = 0.05
resvec.pmLabelBarWidthF = 0.6

# draw the vectors
vc = Ngl.vector(wks, u, v, resvec) # Draw a vector plot of

########################################################### drawing of the shape buffers
thick= 10

# Plot seamounts buffers
dict_seamounts = read_shape('final_shapes/run_buffer2.shp')
respoly1 = Ngl.Resources()
respoly1.gsLineColor = 'red'
respoly1.gsLineThicknessF = thick
for k in dict_seamounts.keys():
    lontemp, lattemp = dict_seamounts[k]['lon'], dict_seamounts[k]['lat']
    Ngl.add_polyline(wks, vc, lontemp, lattemp, respoly1)

# Plot seamounts buffers
dict_seamounts = read_shape('final_shapes/mauritius_buffer2.shp')
respoly2 = Ngl.Resources()
respoly2.gsLineThicknessF = thick
respoly2.gsLineColor = 'orange'
for k in dict_seamounts.keys():
    lontemp, lattemp = dict_seamounts[k]['lon'], dict_seamounts[k]['lat']
    Ngl.add_polyline(wks, vc, lontemp, lattemp, respoly2)

dict_seamounts = read_shape('final_shapes/mada_buffer2.shp')
respoly3 = Ngl.Resources()
respoly3.gsLineThicknessF = thick
respoly3.gsLineColor = 136
for k in dict_seamounts.keys():
    lontemp, lattemp = dict_seamounts[k]['lon'], dict_seamounts[k]['lat']
    Ngl.add_polyline(wks, vc, lontemp, lattemp, respoly3)

dict_seamounts = read_shape('final_shapes/Moz_buffer2.shp')
respoly4 = Ngl.Resources()
respoly4.gsLineThicknessF = thick
respoly4.gsLineColor = 'cyan'
for k in dict_seamounts.keys():
    lontemp, lattemp = dict_seamounts[k]['lon'], dict_seamounts[k]['lat']
    lontemp = lontemp[:-13]
    lattemp = lattemp[:-13]
    lontemp = lontemp[48:]
    lattemp = lattemp[48:]
    Ngl.add_polyline(wks, vc, lontemp, lattemp, respoly4)

dict_seamounts = read_shape('final_shapes/SA_buffer2.shp')
respoly5 = Ngl.Resources()
respoly5.gsLineThicknessF = thick
respoly5.gsLineColor = 'magenta'
for k in dict_seamounts.keys():
    lontemp, lattemp = dict_seamounts[k]['lon'], dict_seamounts[k]['lat']
    lontemp = np.concatenate((lontemp[663:], lontemp[:500]))
    lattemp = np.concatenate((lattemp[663:], lattemp[:500]))
    Ngl.add_polyline(wks, vc, lontemp, lattemp, respoly5)

############################################## drawing of site locations

# creation of new markers
mstring = "b"
fontnum = 19
xoffset = 0.0
yoffset = 0.08
ratio   = 1.5
size    = 1.55
angle   = 0.0

mrk_indices = np.zeros(3, 'i')
mstrings = ["u","z","y"]     # triangle, star, sqaure
fontnums = [34, 35, 35]
yoffsets = [0.4, 0.0, 0.0]
sizes    = [2.0, 1.5, 1.0]
mrk_indices[0] = Ngl.new_marker(wks, mstrings[0], fontnums[0], 0, \
                                        yoffsets[0], 1, sizes[0], 15.)
mrk_indices[1] = Ngl.new_marker(wks, mstrings[1], fontnums[1], 0, \
                                        yoffsets[1], 1, sizes[1], 0.)
mrk_indices[2] = Ngl.new_marker(wks, mstrings[2], fontnums[2], 0, \
                                        yoffsets[2], 1, sizes[2], 0.)

# Plot seamounts buffers
dict_seamounts = read_shape('final_shapes/points_all_buffers1tiersD.shp')
respoly0 = Ngl.Resources()
respoly0.gsLineColor = 'black'
respoly0.gsLineThicknessF = 3
for k in dict_seamounts.keys():
    respoly0.gsMarkerIndex     = 16       # dots
    respoly0.gsMarkerColor     = "black"
    respoly0.gsMarkerSizeF     = 0.012    # twice normal size
    if k in ['Tofo', 'Grand recif de Tulear', 'Morne Brabant', 'Fort Dauphin', 'Mamanjary', 'La Saline', 'Ile Ste Marie', 'Sta Lucia']:
        respoly0.gsMarkerIndex     = mrk_indices[1]
        respoly0.gsMarkerColor     = 137
    lontemp, lattemp = dict_seamounts[k]['lon'], dict_seamounts[k]['lat']
    Ngl.add_polymarker(wks, vc, lontemp.mean(), lattemp.mean(), respoly0)

################################################### drawing of the text label
restxt = Ngl.Resources()
for k in dictlabels.keys():

    restxt.txFont = 30
    restxt.txFontHeightF = 0.015
    restxt.txFontHeightF = 0.013
    restxt.txAngleF = dictlabels[k]['rotation']
    restxt.txFontColor = dictlabels[k]['color']
    lontemp, lattemp = dictlabels[k]['lon'], dictlabels[k]['lat']
    if(dictlabels[k]['weight'] == 'bold'):
        restxt.txFont = 30
        restxt.txFontHeightF = 0.017
    Ngl.add_text(wks, vc, k, lontemp, lattemp, restxt)


########################################## overlay of vector over contour
# draws the map
Ngl.overlay(contour, vc)
Ngl.draw(contour)

############################################################### drawing of the legend

rlist                  = Ngl.Resources()
rlist.vpWidthF          = 0.05
rlist.vpHeightF         = 0.22
rlist.lgItemCount = 7
rlist.lgLabelOffsetF = 0.5
rlist.lgOrientation     = "Vertical"
rlist.lgLineThicknessF  = 10.0
rlist.lgItemTypes = 5* ["Lines"] + 2 * ['Markers'] 
rlist.lgLineColors       = ['red', 'orange', 'deeppink', 'cyan', 'magenta', 'black', 'brown'] 
rlist.lgMarkerColors       = ['red', 'orange', 'deeppink', 'cyan', 'magenta', 'black', 'brown']
rlist.lgMarkerIndexes = [16] * 6 + [18] 
rlist.lgDashIndexes = 7*[0]
rlist.lgPerimFillColor  = 0
rlist.lgPerimFill = True
rlist.lgPerimOn = True
rlist.lgPerimFill = "SolidFill"
rlist.lgLabelFontHeightF = 0.011
rlist.lgLabelJust = "CenterLeft"
rlist.lgBoxMajorExtentF = 0.8
rlist.lgLeftMarginF = 0.2
rlist.lgRightMarginF = 0.2
labels = ['Buffer La Reunion', 'Buffer Mauritius', 'Buffer Madagascar', 'Buffer Mozambique', 'Buffer South Africa', 'Seamounts', 'Coastal sites']
leg = Ngl.legend_ndc(wks, len(labels), labels, 0.685, 0.467, rlist)

# add a page to the pdf output
Ngl.frame(wks)

Ngl.end()
