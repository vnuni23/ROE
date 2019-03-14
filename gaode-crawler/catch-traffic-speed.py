#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os,sys,time,string
import urllib
import json,requests,math

import LocaDiv
import coordTrans
import datetime

apikey=''  ###
citycode='440100'    ## 440100 = GZ

print("Begin !")
start_time=time.time()

target_area=('113.299,23.115,113.332,23.152')    #left bottom / right top

loc=LocaDiv.LocaDiv(target_area)
locs=loc.ls_row()

if locs == []:
   locs = ([target_area])

path='./output'
#grid='113.299,23.115;113.332,23.152'

catch_time=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
print(catch_time)
f1=open(path+'/traffic_coord_'+catch_time+'.csv','wt',encoding='utf-8')
f2=open(path+'/traffic_status_'+catch_time+'.csv','wt',encoding='utf-8')
f3=open(path+'/traffic_segment_'+catch_time+'.csv','wt',encoding='utf-8')

count=0

for loc in locs:
    loca=(loc.split(',')[0] + ',' + loc.split(',')[1] + ';' + loc.split(',')[2] + ',' + loc.split(',')[3])
    print('loca = ' + loca)
    url=('https://restapi.amap.com/v3/traffic/status/rectangle?key=' + apikey + '&rectangle=' + str(loca) + 
        '&adcode=' + citycode + '&extensions=all&output=json')
    print('URL:' + url)
    json_obj = requests.get(url)
    data=json_obj.json()
    rployline=[]

    print('infocode = ' + data['infocode'])
    # time.sleep(1)
    f3.write('rname,rdirection,rangle,rspeed,x_s,y_s,x_e,y_e \n')
    for road in data['trafficinfo']['roads']:
        # print(road)
        count=count + 1
        trafficstatus=str(count) + ',' + str(road) + '\n'
        f2.write(trafficstatus)
        
        try:
            rname=road['name']
        except KeyError:
            rname= 'NaN'

        try:
            rdirection=road['direction']
        except KeyError:
            rdirection= 'NaN'

        try:
            rangle=road['angle']
        except KeyError:
            rangle= 'NaN'
        
        try:
            rspeed=road['speed']
        except KeyError:
            rspeed= 'NaN'

        try:
            rpolyline=road['polyline'].split(';')
        except KeyError:
            rpolyline= 'NaN'

        if rpolyline != 'NaN':
           rpolyline_wgs84_x=[0]*len(rpolyline)
           rpolyline_wgs84_y=[0]*len(rpolyline)
           #print(rpolyline_wgs84_x,rpolyline_wgs84_y)

           for i in range(0,len(rpolyline)):
               rpolyline_wgs84_x[i]=float(rpolyline[i].split(',')[0])
               rpolyline_wgs84_y[i]=float(rpolyline[i].split(',')[1])
               #print(float(rpolyline[i].split(',')[0]),float(rpolyline[i].split(',')[1]))
               rpolyline_wgs84_x[i],rpolyline_wgs84_y[i] = coordTrans.gcj02_to_wgs84(float(rpolyline[i].split(',')[0]),float(rpolyline[i].split(',')[1]))
               #print(rpolyline_wgs84_x[i],rpolyline_wgs84_y[i])
               Roadloc=rname + ',' + rdirection + ',' + rangle + ',' + rspeed + ',' + str(rpolyline_wgs84_x[i]) + ',' + str(rpolyline_wgs84_y[i]) + '\n'
               f1.write(Roadloc)

               if i != 0:
                  Roadloc_s=rname + ',' + rdirection + ',' + rangle + ',' + rspeed + ',' + str(rpolyline_wgs84_x[i-1]) + ',' + str(rpolyline_wgs84_y[i-1]) + ',' + str(rpolyline_wgs84_x[i]) + ',' + str(rpolyline_wgs84_y[i]) + '\n' 
                  f3.write(Roadloc_s)
               

               # del rpolyline_wgs84_x,rpolyline_wgs84_y

f1.close()
f2.close()
f3.close()
end_time = time.time()

print("数据抓取完毕，用时%.2f秒" % (end_time - start_time))
print(" ")
