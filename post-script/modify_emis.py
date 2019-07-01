#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,sys
import math,re
import numpy as np
import datetime,time
import scipy.io as scio

work_path = './ROE_V1.0/'
data_path= work_path + '/calculation/emission_hour/'
output_path = work_path + '/calculation/emission_hour/'

road_map_file='/base_info/base_road_map.csv'
f_basemap = open(work_path + road_map_file, 'r', encoding='utf-8')

x_s=[];y_s=[];x_e=[];y_e=[];base_coord=[];
fclass=[];oneway=[];street_length=[];


for line in f_basemap.readlines()[1:]:
    # print(line)
    x_s.append(line.split(',')[4])
    y_s.append(line.split(',')[5])
    x_e.append(line.split(',')[6])
    y_e.append(line.split(',')[7])
    base_coord.append(re.split(',|\n',line)[4:8])

    fclass.append(line.split(',')[19])
    oneway.append(line.split(',')[22])
    street_length.append(re.split(',|\n',line)[27])

f_basemap.close()

#species_flag=['VOC','CO','NOx','PM Exhaust']
species_flag=['CO','HC','NOx','PM25','PM10']


start_day=datetime.datetime(2018,5,5)
end_day=datetime.datetime(2018,5,6)

span_day=(end_day-start_day).days+1

for n in range(span_day):
    cal_day = start_day + datetime.timedelta(days=n)
    start_time = time.time()

    emis_format = np.zeros((len(base_coord), 51, 24))
    emis_input = np.zeros((len(base_coord), 24, len(species_flag)))

    for s in range(len(species_flag)):

        emis_input[:, :, s] = np.loadtxt(data_path  \
                                         + str(cal_day.year).zfill(4) + '-' + str(cal_day.month).zfill(2) + '-' + str(cal_day.day).zfill(2) \
                                         + '_hour_emission_' + species_flag[s] + '.txt', \
                                         delimiter=',', skiprows=(1))
    for h in range(24):
        print('nday=' + str(n + 1) + '; hour=' + str(h))

        for l in range(len(base_coord)):
            emis_format[l, 0, h] = l + 1
            emis_format[l, 1, h] = l + 1
            emis_format[l, 2, h] = 20
            emis_format[l, 3, h] = float(x_s[l])
            emis_format[l, 4, h] = float(y_s[l])
            emis_format[l, 5, h] = float(x_e[l])
            emis_format[l, 6, h] = float(y_e[l])

            emis_format[l, 8, h] = emis_input[l, h, 1] * 1.e6
            emis_format[l, 9, h] = emis_input[l, h, 0] * 1.e6
            emis_format[l,10, h] = emis_input[l, h, 2] * 1.e6

        emis_format[np.isnan(emis_format)] = 0

        ## adapt LST to GMT
        # if h<16:
        #     save_output1 = np.savetxt(work_path + 'MUNICH_emis/EL.traf.' \
        #                               + str(cal_day.year).zfill(4)  + str(cal_day.month).zfill(2)  + str(cal_day.day).zfill(2)  + str(h+8).zfill(2), \
        #                               emis_format[:, :, h], fmt='%i %i %i %.10f %.10f %.10f %.10f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f', delimiter=',', \
        #                               header='i idbrin typo xa ya xb yb  CH4       NMHC      CO        NOx       PA        FC         SO2       CO2       BE        EC         OM        NO2        TSP       PM10       PM25      PM1        IP        BkF          BbF          BghiP        Fl           BaP          Py           BjF          BaA          Chr          Phe          Ant          DahA         BeP          As           Cd           Cr           Cu           Hg           Ni           Pb           Se           Zn           Al           Ti           Fe           Ba           Si ', \
        #                               newline='\n')
        # else:
        #     save_output2 = np.savetxt(work_path + 'MUNICH_emis/EL.traf.' \
        #                               + str(cal_day.year).zfill(4) + str(cal_day.month).zfill(2) + str(cal_day.day).zfill(2) + str(h - 16).zfill(2), \
        #                               emis_format[:, :, h], fmt='%i %i %i %.10f %.10f %.10f %.10f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f', delimiter=',', \
        #                               header='i idbrin typo xa ya xb yb  CH4       NMHC      CO        NOx       PA        FC         SO2       CO2       BE        EC         OM        NO2        TSP       PM10       PM25      PM1        IP        BkF          BbF          BghiP        Fl           BaP          Py           BjF          BaA          Chr          Phe          Ant          DahA         BeP          As           Cd           Cr           Cu           Hg           Ni           Pb           Se           Zn           Al           Ti           Fe           Ba           Si ', \
        #                               newline='\n')

        ## no adapt LST to GMT
        save_output1 = np.savetxt(output_path \
                                      + str(cal_day.year).zfill(4)  + str(cal_day.month).zfill(2)  + str(cal_day.day).zfill(2)  + str(h).zfill(2), \
                                      emis_format[:, :, h], fmt='%i %i %i %.10f %.10f %.10f %.10f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f', delimiter=',', \
                                      header='i idbrin typo xa ya xb yb  CH4       NMHC      CO        NOx       PA        FC         SO2       CO2       BE        EC         OM        NO2        TSP       PM10       PM25      PM1        IP        BkF          BbF          BghiP        Fl           BaP          Py           BjF          BaA          Chr          Phe          Ant          DahA         BeP          As           Cd           Cr           Cu           Hg           Ni           Pb           Se           Zn           Al           Ti           Fe           Ba           Si ', \
                                      newline='\n')