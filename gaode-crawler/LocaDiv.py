#!/usr/bin/python3
# -*- coding: utf-8 -*-

####  API limitation of Gaode map: grid size should be less than 10km x 10km (about 0.1 degree x 0.1 degree)

class LocaDiv(object):

    def __init__(self, loc_all):
        self.loc_all = loc_all

    def lon_all(self):
        lon_len = 0.05 # 0.05 is lon length of division in degree,could be revised

        lon_sw = float(self.loc_all.split(',')[0])
        lon_ne = float(self.loc_all.split(',')[2])
        lon_list = []
        for i in range(0, 1+ int((lon_ne - lon_sw ) / lon_len)):
            lon_list.append(lon_sw + lon_len * i)
        # lon_list.append(lon_ne)
        return lon_list

    def lat_all(self):
        lat_len = 0.05 # 0.05 is lat length of division in degree,could be revised

        lat_sw = float(self.loc_all.split(',')[1])
        lat_ne = float(self.loc_all.split(',')[3])
        lat_list = []
        for i in range(0, 1+ int((lat_ne - lat_sw ) / lat_len)):
            lat_list.append(lat_sw + lat_len * i)
        # lat_list.append(lat_ne)
        return lat_list

    def ls_row(self):
        l1 = self.lon_all()
        l2 = self.lat_all()
        ls = []
        for x in range(0, len(l1) - 1):
            for y in range(0 , len(l2) - 1):
                ab = str(l1[x]) + ',' + str(l2[y]) + ',' + str(l1[x+1]) + ',' + str(l2[y+1])
                ls.append(ab)
        return ls

####

