# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 16:17:11 2022

@author: rps207
"""

# Plot up MAXSS data

import netCDF4 as nc
import cartopy.crs as ccrs;
import matplotlib.pyplot as plt;
from matplotlib import colorbar, colors;
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER;
import cartopy.feature as cfeature
from netCDF4 import date2num, num2date, Dataset
import cv2
import gc
cmap_reversed = plt.cm.get_cmap('inferno')


import os
directory = 'C:\\Users\\rps207\\Documents\\Python\\2022-MAXSS\\output\\MAXSS_RUN\\maxss\\storm-atlas\\ibtracs\\north-atlantic\\2010\\2010176N16278_AL012010_ALEX'
iframe=1000
for filename in os.listdir(directory):
    if filename.endswith(".nc"):
        
        #do smth
        
        
        path="C:\\Users\\rps207\\Documents\\Python\\2022-MAXSS\\output\\MAXSS_RUN\\maxss\\storm-atlas\\ibtracs\\north-atlantic\\2010\\\\2010176N16278_AL012010_ALEX\\"
        
        fullpath=os.path.join(path, filename)
        MAXSS_nc = nc.Dataset(fullpath)
        #MAXSS_ = MAXSS_nc.variables
        MAXSS_lat = MAXSS_nc.variables['latitude'][:]
        MAXSS_lon = MAXSS_nc.variables['longitude'][:]
        MAXSS_time = MAXSS_nc.variables['time'][:]
        MAXSS_dates = num2date(MAXSS_time, MAXSS_nc.variables['time'].units)

        
        for hour_step in range(0, len(MAXSS_time)-1):
            #print(hour_step)
            iframe=iframe+1   
    
            MAXSS_Wind = MAXSS_nc.variables['WS1_mean'][hour_step,:,:]
            MAXSS_Flux = MAXSS_nc.variables['OF'][hour_step,:,:]
            MAXSS_time_hour=MAXSS_time[hour_step]
            MAXSS_dates_hour=MAXSS_dates[hour_step]

            maxvar_wind = 30#np.nanmax(MAXSS_Wind);
            minvar_wind = 0#np.nanmin(MAXSS_Wind); 
            
            maxvar_flux = 0.5 #np.nanmax(MAXSS_Flux);
            minvar_flux = -0.1 #np.nanmin(MAXSS_Flux); 

            #this plots the data as 1 x 1 grids 
            
            fig41=plt.figure(figsize=(18,24))
            gs = fig41.add_gridspec(50, 1)
            
            ticksize = 30;
            labelsize = 40;
            fig41_ax = fig41.add_subplot(gs[1:24,0:1],projection=ccrs.PlateCarree());
            data_proj = ccrs.PlateCarree()
            gl = fig41_ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.25, linestyle='--');
            contPlot = plt.pcolormesh(MAXSS_lon, MAXSS_lat, MAXSS_Wind, transform=data_proj ,  cmap=cmap_reversed,vmin=minvar_wind, vmax=maxvar_wind);
            gl.xlabels_top = False;
            gl.ylabels_right = False;
            gl.xformatter = LONGITUDE_FORMATTER;
            gl.yformatter = LATITUDE_FORMATTER;
            gl.xlabel_style = {'size': ticksize};
            gl.ylabel_style = {'size': ticksize};            
            plt.xlabel("Longitude($^\circ$)", fontsize=labelsize);
            plt.ylabel("Latitude($^\circ$)", fontsize=labelsize);
            fig41_ax.coastlines();
            resol = '50m'  # use data at this scale
            land = cfeature.NaturalEarthFeature('physical', 'land', \
            scale=resol, edgecolor='k', facecolor=cfeature.COLORS['land']);
            fig41_ax.add_feature(land, facecolor='beige')
            fig41_ax.set_xlabel("Longitude($^\circ$)", fontsize=30);
            fig41_ax.set_ylabel("Latitude($^\circ$)", fontsize=30);
            m = plt.cm.ScalarMappable(cmap=cmap_reversed)
            m.set_array(MAXSS_Wind)
            m.set_clim(minvar_wind, maxvar_wind)
            cb = plt.colorbar(m); #, boundaries=np.linspace(0, 2, 6))   
            cb.ax.tick_params(labelsize=30)
            cb.set_label("Wind Speed ($ms^{-1}$)", fontsize=30);
            
            fig41_ax.text(-0.13, 0.55, 'Latitude $(^{\circ})$', va='bottom', ha='center',
                rotation='vertical', rotation_mode='anchor',fontsize=30,
                transform=fig41_ax.transAxes)
            fig41_ax.text(0.5, -0.13, 'Longitude $(^{\circ})$', va='bottom', ha='center',
                rotation='horizontal', rotation_mode='anchor',fontsize=30,
                transform=fig41_ax.transAxes)            
            fig41_ax.text(0.5, 1.05, "Time = {0}".format(MAXSS_dates_hour), va='bottom', ha='center',
                rotation='horizontal', rotation_mode='anchor',fontsize=30,
                transform=fig41_ax.transAxes)   
            
            fig41_ax2 = fig41.add_subplot(gs[26:49,0:1],projection=ccrs.PlateCarree());
            data_proj = ccrs.PlateCarree()
            gl = fig41_ax2.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='gray', alpha=0.25, linestyle='--');
            contPlot2 = plt.pcolormesh(MAXSS_lon, MAXSS_lat, MAXSS_Flux, transform=data_proj ,  cmap=cmap_reversed,vmin=minvar_flux, vmax=maxvar_flux);
            gl.xlabels_top = False;
            gl.ylabels_right = False;
            gl.xformatter = LONGITUDE_FORMATTER;
            gl.yformatter = LATITUDE_FORMATTER;
            gl.xlabel_style = {'size': ticksize};
            gl.ylabel_style = {'size': ticksize};            
            plt.xlabel("Longitude($^\circ$)", fontsize=labelsize);
            plt.ylabel("Latitude($^\circ$)", fontsize=labelsize);
            fig41_ax2.coastlines();
            resol = '50m'  # use data at this scale
            land = cfeature.NaturalEarthFeature('physical', 'land', \
            scale=resol, edgecolor='k', facecolor=cfeature.COLORS['land']);
            fig41_ax2.add_feature(land, facecolor='beige')
            fig41_ax2.set_xlabel("Longitude($^\circ$)", fontsize=30);
            fig41_ax2.set_ylabel("Latitude($^\circ$)", fontsize=30);
            
            m2 = plt.cm.ScalarMappable(cmap=cmap_reversed)
            m2.set_array(MAXSS_Flux)
            m2.set_clim(minvar_flux, maxvar_flux)
            cb = plt.colorbar(m2); #, boundaries=np.linspace(0, 2, 6))   
            cb.ax.tick_params(labelsize=30)
            cb.set_label("CO$_{2}$ flux (g C $m^{-2}$ $day^{-1}$)", fontsize=30);
            
            
            fig41_ax2.text(-0.13, 0.55, 'Latitude $(^{\circ})$', va='bottom', ha='center',
                rotation='vertical', rotation_mode='anchor',fontsize=30,
                transform=fig41_ax2.transAxes)
            fig41_ax2.text(0.5, -0.13, 'Longitude $(^{\circ})$', va='bottom', ha='center',
                rotation='horizontal', rotation_mode='anchor',fontsize=30,
                transform=fig41_ax2.transAxes)      
            
            from pathlib import Path
            SAVPATH=("C:\\Users\\rps207\\Documents\\Python\\2022-MAXSS\\output\plots\\\MAXSS_RUN\\maxss\\storm-atlas\\ibtracs\\north-atlantic\\2010\\2010176N16278_AL012010_ALEX\\")
            if not os.path.exists(SAVPATH):
                os.makedirs(SAVPATH)
            plt.close()
            plt.clf()
            fig41.savefig("C:\\Users\\rps207\\Documents\\Python\\2022-MAXSS\\output\plots\\\MAXSS_RUN\\maxss\\storm-atlas\\ibtracs\\north-atlantic\\2010\\2010176N16278_AL012010_ALEX\\frame_{0}_frame_maxss_alex.png".format(format(iframe, "03d")));
            gc.collect
    else:
        print("didnt work")
else:
    print("didnt work")

import os
#### Create video from images    
image_folder = ("C:\\Users\\rps207\\Documents\\Python\\2022-MAXSS\\output\plots\\\MAXSS_RUN\\maxss\\storm-atlas\\ibtracs\\north-atlantic\\2010\\2010176N16278_AL012010_ALEX\\")
video_name = "MAXSS_ALEX_2010_SHORT.avi"

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 2, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()