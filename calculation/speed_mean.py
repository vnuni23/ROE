#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,sys
import math,re
import numpy as np
import datetime,time,string

# input the date here (without zero)
start_day=datetime.datetime(2018,5,5)
end_day=datetime.datetime(2018,5,6)

span_day=(end_day-start_day).days+1

step_in_hour=12   #   ex. 12 = catch data in every 5-minutes



work_path='./ROE_V1.0/'
data_path= work_path + 'gaode-crawler/output/'

x_s=[];y_s=[];x_e=[];y_e=[]
base_coord=[]
f_basemap = open(work_path + '/base_info/base_traffic_map_modified_withroad_length.csv', 'r', encoding='utf-8')
for line in f_basemap.readlines()[1:]:
    # print(line)
    x_s.append(line.split(',')[4])
    y_s.append(line.split(',')[5])
    x_e.append(line.split(',')[6])
    y_e.append(line.split(',')[7])
    base_coord.append(re.split(',|\n',line)[4:8])
f_basemap.close()


for n in range(span_day):
    speed_hour=np.full((len(base_coord),24),np.nan)
    for h in range(24):
        print('nday=' + str(n + 1) + '; hour=' + str(h))
        cal_day=start_day+datetime.timedelta(days=n,hours=h)
        # speed_step = [[0.0 for x in range(step_in_hour)] for y in range(len(base_coord))]
        speed_step = np.full((len(base_coord),step_in_hour),np.nan)
        for s in range(step_in_hour):
            print('step = ' + str(s))
            start_time=time.time()
            f_input=open(data_path+'traffic_segment_' \
                         +str(cal_day.year).zfill(4)+'-'+str(cal_day.month).zfill(2)+'-'+str(cal_day.day).zfill(2) \
                         +'_'+str(cal_day.hour).zfill(2)+'-'+str(cal_day.minute+s*5).zfill(2)+'.csv','r',encoding='utf-8')


            for traffic_coord in f_input.readlines()[1:]:
                for l_base in range(len(base_coord)):
                    # if re.split(',|\n',traffic_coord)[4:8] == base_coord[l_base]:
                    #     # print('l_base = ' + str(l_base))
                    #     speed_step[l_base][s]=float(re.split(',|\n',traffic_coord)[3])
                    #     # print(speed_step)
                    if re.split(',|\n',traffic_coord)[4][0:12] == x_s[l_base][0:12] and \
                            re.split(',|\n',traffic_coord)[5][0:11] == y_s[l_base][0:11] and \
                            re.split(',|\n', traffic_coord)[6][0:12] == x_e[l_base][0:12] and \
                            re.split(',|\n', traffic_coord)[7][0:11] == y_e[l_base][0:11]:
                        speed_step[l_base][s] = float(re.split(',|\n', traffic_coord)[3])
                        # print(l_base)
                        break

            end_time=time.time()
            print('spend %.2f s' % (end_time - start_time))
        speed_hour[:,h]=np.nanmean(speed_step,1).reshape((len(base_coord),))
    print(speed_hour)
    save_output1=np.savetxt(work_path + '/result/speed_hour/' \
                            +str(cal_day.year).zfill(4)+'-'+str(cal_day.month).zfill(2)+'-'+str(cal_day.day).zfill(2)+'_hour_speed.txt', \
                            speed_hour,fmt='%2f',delimiter=',',header='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23', \
                            newline='\n')

