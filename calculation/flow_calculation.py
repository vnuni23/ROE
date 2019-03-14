#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,sys
import math,re
import numpy as np
import datetime,time,string

work_path = './ROE_V1.0/'
data_path= work_path + 'gaode-crawler/output/'

f_basemap = open(work_path + '/base_info/base_traffic_map_modified_withroad_length.csv', 'r', encoding='utf-8')

x_s=[];y_s=[];x_e=[];y_e=[];base_coord=[];
fclass=[];oneway=[];length=[];


for line in f_basemap.readlines()[1:]:
    # print(line)
    x_s.append(line.split(',')[4])
    y_s.append(line.split(',')[5])
    x_e.append(line.split(',')[6])
    y_e.append(line.split(',')[7])
    base_coord.append(re.split(',|\n',line)[4:8])

    fclass.append(line.split(',')[19])
    oneway.append(line.split(',')[22])
    length.append(re.split(',|\n',line)[27])

f_basemap.close()

start_day=datetime.datetime(2018,5,5)
end_day=datetime.datetime(2018,5,6)

span_day=(end_day-start_day).days+1

for n in range(span_day):
    cal_day = start_day + datetime.timedelta(days=n)
    speed_data=np.loadtxt(work_path + 'result/speed_hour/' \
                          +str(cal_day.year).zfill(4)+'-'+str(cal_day.month).zfill(2)+'-'+str(cal_day.day).zfill(2)+'_hour_speed.txt', \
                          delimiter = ',', skiprows = (1))
    flow_data = np.full((len(base_coord), 24), np.nan)

    for h in range(24):
        start_time = time.time()
        print('nday=' + str(n + 1) + '; hour=' + str(h))
        for l in range(len(base_coord)):

            ### Macroscopic fundamental diagram data can be updated

            k = [358.7865,201.5,227.002]
            uf = [69.29,58.98,38.50]

            if fclass[l] == 'motorway' or fclass[l] == 'motorway_link':
                if speed_data[l, h] > uf[0]:
                    speed_data[l, h] = uf[0]

                flow_data[l, h] = k[0] * speed_data[l, h] * math.log(uf[0] / speed_data[l, h])

            elif fclass[l] == 'trunk' or fclass[l] == 'trunk_link':
                if speed_data[l, h] > uf[1]:
                    speed_data[l, h] = uf[1]

                flow_data[l, h] = k[1] * speed_data[l, h] * math.log(uf[1] / speed_data[l, h])

            elif fclass[l] == 'primary' or fclass[l] == 'primary_link':
                if speed_data[l, h] > uf[2]:
                    speed_data[l, h] = uf[2]

                flow_data[l, h] = k[2] * speed_data[l, h] * math.log(uf[2] / speed_data[l, h])

            elif fclass[l] == 'secondary' or fclass[l] == 'secondary_link':
                if speed_data[l, h] > uf[2]:
                    speed_data[l, h] = uf[2]

                flow_data[l, h] = k[2] * speed_data[l, h] * math.log(uf[2] / speed_data[l, h])

            elif fclass[l] == 'tertiary' or fclass[l] == 'tertiary_link':
                if speed_data[l, h] > uf[2]:
                    speed_data[l, h] = uf[2]

                flow_data[l, h] = k[2] * speed_data[l, h] * math.log(uf[2] / speed_data[l, h])

            else:
                if speed_data[l, h] > uf[2]:
                    speed_data[l, h] = uf[2]

                flow_data[l, h] = k[2] * speed_data[l, h] * math.log(uf[2] / speed_data[l, h])

        end_time = time.time()
        print('spend %.2f s' % (end_time - start_time))

    print(flow_data)
    save_output1 = np.savetxt(work_path + 'result/flow_hour/' \
                              + str(cal_day.year).zfill(4) + '-' + str(cal_day.month).zfill(2) + '-' + str(cal_day.day).zfill(2) + '_hour_flow.txt', \
                              flow_data, fmt='%2f', delimiter=',',header='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23', \
                              newline='\n')