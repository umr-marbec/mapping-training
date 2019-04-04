import Ngl

wks_type = "png"
wks = Ngl.open_wks(wks_type, "conmasklc")

res = Ngl.Resources()

res.nglDraw = False
res.nglFrame = False

res.mpProjection        = "LambertConformal"

res.mpLimitMode         = "LatLon"     # limit map via lat/lon
res.mpMinLatF           =  10.         # map area
res.mpMaxLatF           =  75.         # latitudes
res.mpMinLonF           =  60.         # and
res.mpMaxLonF           = 165.         # longitudes

res.nglMaskLambertConformal = True
res.nglMaskLambertConformalOutlineOn = True

res.tiMainString         = "Map example"
res.tiMainFontHeightF    = 0.010

map = Ngl.map(wks,res)

Ngl.draw(map)
Ngl.frame(wks)
