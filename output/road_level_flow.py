#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,sys
import math,re
import numpy as np
import datetime,time
import scipy.io as scio

import ef_equation

work_path = './ROE_V1.0/'
data_path= work_path + 'gaode-crawler/output/'

f_basemap = open(work_path + '/base_info/base_traffic_map_modified_withroad_length.csv', 'r', encoding='utf-8')

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


road_level=['motorway','trunk','primary','secondary','tertiary']
road_level_link=['motorway_link','trunk_link','primary_link','secondary_link','tertiary_link']


start_day=datetime.datetime(2018,5,5)
end_day=datetime.datetime(2018,5,6)

span_day=(end_day-start_day).days+1

for n in range(span_day):
    cal_day = start_day + datetime.timedelta(days=n)
    flow_data=np.loadtxt(work_path + '/flow_hour/' \
                          +str(cal_day.year).zfill(4)+'-'+str(cal_day.month).zfill(2)+'-'+str(cal_day.day).zfill(2)+'_hour_flow.txt', \
                          delimiter = ',', skiprows = (1))

    road_type_flow = np.full((len(base_coord), 24, len(road_level)), np.nan)
    road_type_flow_ave = np.full((len(road_level), 24), np.nan)

    for l in range(len(base_coord)):
        if fclass[l] == 'motorway' or fclass[l] == 'motorway_link':
            road_type_flow[l, :, 0] = flow_data[l, :]

        elif fclass[l] == 'trunk' or fclass[l] == 'trunk_link':
            road_type_flow[l, :, 1] = flow_data[l, :]

        elif fclass[l] == 'primary' or fclass[l] == 'primary_link':
            road_type_flow[l, :, 2] = flow_data[l, :]

        elif fclass[l] == 'secondary' or fclass[l] == 'secondary_link':
            road_type_flow[l, :, 2] = flow_data[l, :]

        else:
            road_type_flow[l, :, 2] = flow_data[l, :]

    for t in range(len(road_level)):
        road_type_flow_ave[t, :] = np.nanmean(road_type_flow[:, :, t], 0)

    print(road_type_flow_ave)

    save_output1 = np.savetxt(work_path + 'result/flow_hour/' \
                              + str(cal_day.year).zfill(4) + '-' + str(cal_day.month).zfill(2) + '-' \
                              + str(cal_day.day).zfill(2) + '_road_type_flow_ave.txt', \
                              road_type_flow_ave, fmt='%2f', delimiter=',', \
                              header='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23', \
                              newline='\n')



