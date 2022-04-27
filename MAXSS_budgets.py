# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:50:18 2022

Allowing integrated fluxes to be calculated for custom runs with 
variable temporal and spatial resolutions. 

Note: that this script is essentially a replacement for flux_budgets
which is only setup for monthly runs

@author: rps207
"""

#### Import packages





    


#### Solutions for calculating areas on the earths surface

    #### stack overflow sinusoidal projection
#https://stackoverflow.com/questions/4681737/how-to-calculate-the-area-of-a-polygon-on-the-earths-surface-using-python
        def reproject(latitude, longitude):
            """Returns the x & y coordinates in meters using a sinusoidal projection"""
            from math import pi, cos, radians
            earth_radius = 6378137 # in meters
            lat_dist = pi * earth_radius / 180.0
        
            y = [lat * lat_dist for lat in latitude]
            x = [long * lat_dist * cos(radians(lat)) 
                        for lat, long in zip(latitude, longitude)]
            return x, y
        
        
        def area_of_polygon(x, y):
            """Calculates the area of an arbitrary polygon given its verticies"""
            area = 0.0
            for i in range(-1, len(x)-1):
                area += x[i] * (y[i+1] - y[i-1])
            return abs(area) / 2.0


latitude = [0, 0, 1, 1, 0]
longitude = [39, 40, 40, 39,39]
x,y=reproject(latitude, longitude)
area_of_polygon(x, y)
#12391085347.451996

    #### peters solution - is there a reference or even a source for this?
        def get_grid_area_1deg(latDegrees):
           # area of a 1x1 degree box at a given latitude in radians
           latRadians = latDegrees * dtor
           cosLat, sinLat = cos(latRadians), sin(latRadians)
           rc, rs = re * cosLat, rp * sinLat
           r2c, r2s = re * re * cosLat, rp * rp * sinLat
           earth_radius = sqrt((r2c * r2c + r2s * r2s) / (rc * rc + rs * rs))
           erd = earth_radius * dtor
           return erd * erd * cosLat
        # Define constants
        #Earth equatorial and polar radii in km
        from math import sqrt, cos, sin, radians
        re, rp = 6378.137,6356.7523
        dtor = radians(1.)
        get_grid_area_1deg(7)
        #12392.029030473717


    #### pyproj solution
from pyproj import Geod
from timeit import default_timer as timer

start = timer()
#geod = Geod('+a=6378137')                               #gives ->12391714368.859478 - THIS ASSUMES A SPHERE
#geod = Geod('+a=6378137 +b=6356752')                     #gives ->12308777144.780497
#geod = Geod('+a=6378137 +f=0.0033528106647475126')       #gives -> 12308778361.469454
#geod = Geod(ellps='WGS84')                               #gives -> 12308778361.469452

lats = [0, 0, 1, 1, 0]
lons = [39, 40, 40, 39,39]
poly_area, poly_perimeter = geod.polygon_area_perimeter(lons, lats)
print("area: {} , perimeter: {}".format(poly_area, poly_perimeter))
end = timer()
print(end - start) # Time in seconds, e.g. 5.38091952400282


    #### pyproj shapely solution
        def calc_area(lis_lats_lons):
            import numpy as np
            from pyproj import Proj
            from shapely.geometry import shape
            lons, lats = zip(*lis_lats_lons)
            ll = list(set(lats))[::-1]
            var = []
            for i in range(len(ll)):
                var.append('lat_' + str(i+1))
            st = ""
            for v, l in zip(var,ll):
                st = st + str(v) + "=" + str(l) +" "+ "+"
            st = st +"lat_0="+ str(np.mean(ll)) + " "+ "+" + "lon_0" +"=" + str(np.mean(lons))
            tx = "+proj=aea +" + st
            pa = Proj(tx)
            x, y = pa(lons, lats)
            cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
            return shape(cop).area 

calc_area(lis_lats_lons = [(39, 0.0),
     (40, 0.0),
     (40, 1.0),
     (39, 1.0),
     (39, 0.0)])

#12308463846.393326

    #### pyproj shapely solution 
#https://gis.stackexchange.com/questions/127607/calculating-area-in-km%C2%B2-for-polygon-in-wkt-using-python
import pyproj    
import shapely
import shapely.ops as ops
from shapely.geometry.polygon import Polygon
from functools import partial


geom = Polygon([[-180,0],[-180,1],[-179,1],[-179,0],[-180,0]])
geom_area = ops.transform(
    partial(
        pyproj.transform,
        pyproj.Proj(init='EPSG:4326'), # World Geodetic System 1984 , https://pyproj4.github.io/pyproj/stable/gotchas.html
        pyproj.Proj(
            proj='aea',
            lat_1=geom.bounds[1],
            lat_2=geom.bounds[3]
        )
    ),
    geom)

# Print the area in m^2
print(geom_area.area)
#12308463846.39476



    #### Calculate the area inside of any GeoJSON geometry. This is a port of Mapbox's geojson-area for Python.
#https://github.com/scisco/area
from area import area
obj = {'type':'Polygon','coordinates':[[[39,0],[39,1],[40,1],[40,0],[39,0]]]}
area(obj)
#12391399902.071121







