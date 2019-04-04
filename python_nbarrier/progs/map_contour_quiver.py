import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# map initialisation
m = Basemap(llcrnrlon=np.min(lon), llcrnrlat=np.min(lat),
            urcrnrlon=np.max(lon), urcrnrlat=np.max(lat), 
            projection='cyl', resolution='c')

# conversion from geo. to map coordinate
lon2d, lat2d = np.meshgrid(lon, lat) # needs 2D coord. arrays
x, y = m(lon2d, lat2d)

# map background
m.fillcontinents(color='gray', lake_color='gray')  

# drawing contour lines
cs = m.contour(x, y, z, colors='k', linewidths=0.5)
plt.clabel(cs, fmt='%.2f')

# drawing quiver plot
q = plt.quiver(x, y, u, v, z, cmap=plt.cm.get_cmap('hsv'), scale=1000, zorder=1000)
q.set_clim(0, 50)
cb = m.colorbar(q)
keys = plt.quiverkey(q, -131, 21, 70, 
        'Wind speed\n(50 m/s)', coordinates='data')
