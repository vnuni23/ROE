#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,sys
import math,re
import numpy as np
import datetime,time
import scipy.io as scio

import ef_equation_china

work_path = '/ROE_V1.0/'
base_info_path= work_path + 'base_info/'
road_map_file= base_info_path + 'base_road_map.csv'
data_path= work_path +'/calculation/'
output_path= '/calculation/emission_hour/'

### input data can be updated

vehicle_fleet_flag_segment=['Small','Medium','Large','Small','Medium','Large','Motorcycles 4-stroke 250 - 750 cm³','Urban Buses Standard 15 - 18 t','Small']


vehicle_fleet_flag=['LDV','MDV','HDV','LDT','MDT','HDT','MC','Bus','Taxi']
vehicle_fleet=np.loadtxt(base_info_path + 'vehicle_fleet.csv',delimiter = ',', skiprows = 1,usecols=(1,))

fuel_type_flag=['Petrol','Diesel','LPG']
fuel_type_percentage=np.loadtxt(base_info_path + 'fuel_type_percentage.csv',delimiter = ',', skiprows = 1,usecols=(1,2,3))
fuel_type_percentage=fuel_type_percentage/100

emission_standard_flag=['Pre I','CHINA I','CHINA II','CHINA III','CHINA IV','CHINA V']


emission_standard_percentage=np.loadtxt(base_info_path + 'emission_standard_percentage.csv',delimiter = ',', skiprows = 1,usecols=(1,2,3,4,5,6))
emission_standard_percentage=emission_standard_percentage/100
###


species_flag=['CO','HC','NOx','PM25','PM10']


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


f_emission_factor=open(base_info_path + 'On Road Hot Emission Factor Chinese.csv', 'r', encoding='utf-8')

emission_factor=[];emission_factor_flag=[]
emission_factor_flag.append(re.split(',|\n',f_emission_factor.readline()))

for line in f_emission_factor.readlines():
    emission_factor.append(re.split(',|\n',line))

f_emission_factor.close()

#############
### for test
#l=n=h=s=vf=ft=es=ef=0
#############

high_altitude = False  # whether the altitude is higher than 1500m

### for evporation  in hour
ef1 = 11.6                # evporation emission factor during driving
ef2 = 6.5 / 24 * (3/60)   # evporation emission factor during parking
###


start_day=datetime.datetime(2018,5,6)
end_day=datetime.datetime(2018,5,6)

span_day=(end_day-start_day).days+1




for n in range(span_day):
    start_time_cal = time.time()

    cal_day = start_day + datetime.timedelta(days=n)
    print(cal_day)

    flow_data=np.loadtxt(data_path + '/flow_hour/' \
                          +str(cal_day.year).zfill(4)+'-'+str(cal_day.month).zfill(2)+'-'+str(cal_day.day).zfill(2)+'_hour_flow.txt', \
                          delimiter = ',', skiprows = (1))

    speed_data = np.loadtxt(data_path + '/speed_hour/' \
                            + str(cal_day.year).zfill(4) + '-' + str(cal_day.month).zfill(2) + '-' + str(cal_day.day).zfill(2) + '_hour_speed.txt', \
                            delimiter=',', skiprows=(1))

    total_emission = np.zeros((len(base_coord), 24, len(species_flag), len(vehicle_fleet_flag), len(fuel_type_flag),len(emission_standard_flag)))
    hef = np.zeros((len(base_coord), 24, len(species_flag), len(vehicle_fleet_flag), len(fuel_type_flag),len(emission_standard_flag)))

    for h in range(24):
        print('nday=' + str(n + 1) + '; hour=' + str(h))

        vehicle_fleet_number = {}
        vehicle_fleet_percentage = {}
        for vff in range(len(vehicle_fleet_flag)):
            vehicle_fleet_number[vehicle_fleet_flag[vff]] = vehicle_fleet[vff]

        ### traffic control

        # for Motorcycles
        vehicle_fleet_number['MC'] = 0

        # for trunk
        if 7<=h<=22:
            vehicle_fleet_number['MDT'] = 0
            vehicle_fleet_number['HDT'] = 0
        if 7<=h<=9 or 18<=h<=20:
            vehicle_fleet_number['LDT'] = 0

        # for bus
        if 2 <= h <= 5:
            vehicle_fleet_number['Bus'] = 0

        ###

        total_vehicle_fleet_number = sum(i for i in vehicle_fleet_number.values())
        for vff in range(len(vehicle_fleet_flag)):
            vehicle_fleet_percentage[vehicle_fleet_flag[vff]] = vehicle_fleet_number[vehicle_fleet_flag[vff]] / total_vehicle_fleet_number

        ### calculate the emission factor
        for l in range(len(base_coord)):
        # for l in range(0,11):
        #     print(l)
            for s in range(len(species_flag)):

                ### for Passenger Car
                for vf in range(len(vehicle_fleet_flag[0:3])):
                    for ft in range(len(fuel_type_flag)):
                        for es in range(len(emission_standard_flag)):
                            ### for evaporation
                            if species_flag[s] == 'HC' and fuel_type_flag[ft] == 'Petrol':
                                total_emission[l, h, s, vf, ft, es] = total_emission[l, h, s, vf, ft, es] + (ef1 * float(street_length[l]) /1000 / speed_data[l,h] + ef2) * flow_data[l,h] \
                                                                       * vehicle_fleet_percentage[vehicle_fleet_flag[vf]] * \
                                                                      fuel_type_percentage[vf, ft] * emission_standard_percentage[vf, es]

                            for ef in range(len(emission_factor)):
                                ### for exhaust
                                if emission_factor[ef][0] == 'Passenger Cars' and emission_factor[ef][1] == fuel_type_flag[ft] and \
                                        emission_factor[ef][2] == vehicle_fleet_flag_segment[vf] and emission_factor[ef][3] == emission_standard_flag[es] and \
                                        emission_factor[ef][5] == species_flag[s]:

                                    try:
                                        c_speed = ef_equation_china.speed_correction(speed_data[l,h], species_flag[s], emission_factor[ef][1], emission_standard_flag[es])
                                    except UnboundLocalError:
                                        c_speed = 1

                                    try:
                                        c_ta = ef_equation_china.ta_correction(cal_day.month, species_flag[s], emission_factor[ef][1], vehicle_fleet_flag[vf])
                                    except UnboundLocalError:
                                        c_ta = 1

                                    try:
                                        c_rh = ef_equation_china.rh_correction(cal_day.month, species_flag[s], emission_factor[ef][1])
                                    except UnboundLocalError:
                                        c_rh = 1

                                    if high_altitude:
                                        try:
                                            c_height = ef_equation_china.height_correction(species_flag[s],emission_factor[ef][1],vehicle_fleet_flag[vf])
                                        except UnboundLocalError:
                                            c_height = 1
                                    else:
                                        c_height = 1

                                    # c_speed = c_ta = c_rh = c_height = 1
                                    hef[l,h,s,vf,ft,es] = ef_equation_china.ef_equation_china(float(emission_factor[ef][6]), c_speed, c_ta, c_rh, c_height)
                                    #print(vehicle_fleet_flag[vf], speed_data[l,h], species_flag[s], fuel_type_flag[ft],emission_standard_flag[es], c_speed)

                                    total_emission[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * \
                                                          flow_data[l,h] * vehicle_fleet_percentage[vehicle_fleet_flag[vf]] * \
                                                          fuel_type_percentage[vf, ft] * emission_standard_percentage[vf, es] * \
                                                          float(street_length[l]) /1000

                                    break


                ### for Truck and motorcycle
                for vf in range(len(vehicle_fleet_flag[0:3]), len(vehicle_fleet_flag[0:7])):
                    emission_standard_flag_truck = emission_standard_flag

                    if vehicle_fleet_flag[vf] == 'MC':
                        vehicle_fleet_flag_truck = 'L-Category'
                    else:
                        vehicle_fleet_flag_truck = 'Heavy Duty Trucks'

                    for ft in range(len(fuel_type_flag)):
                        for es in range(len(emission_standard_flag_truck)):
                            ### for evaporation
                            if species_flag[s] == 'HC' and fuel_type_flag[ft] == 'Petrol':
                                total_emission[l, h, s, vf, ft, es] = total_emission[l, h, s, vf, ft, es] + (ef1 * float(street_length[l]) /1000 / speed_data[l,h] + ef2) * flow_data[l,h] \
                                                                       * vehicle_fleet_percentage[vehicle_fleet_flag[vf]] * \
                                                                      fuel_type_percentage[vf, ft] * emission_standard_percentage[vf, es]

                            for ef in range(len(emission_factor)):
                                ### for exhaust
                                if emission_factor[ef][0] == vehicle_fleet_flag_truck and emission_factor[ef][1] == fuel_type_flag[ft] and \
                                        emission_factor[ef][2] == vehicle_fleet_flag_segment[vf] and emission_factor[ef][3] == emission_standard_flag_truck[es] and \
                                        emission_factor[ef][5] == species_flag[s]:


                                    try:
                                        c_speed = ef_equation_china.speed_correction(speed_data[l,h], species_flag[s], emission_factor[ef][1], emission_standard_flag[es])
                                    except UnboundLocalError:
                                        c_speed = 1

                                    try:
                                        c_ta = ef_equation_china.ta_correction(cal_day.month, species_flag[s], emission_factor[ef][1], vehicle_fleet_flag[vf])
                                    except UnboundLocalError:
                                        c_ta = 1

                                    try:
                                        c_rh = ef_equation_china.rh_correction(cal_day.month, species_flag[s], emission_factor[ef][1])
                                    except UnboundLocalError:
                                        c_rh = 1

                                    if high_altitude:
                                        try:
                                            c_height = ef_equation_china.height_correction(species_flag[s],emission_factor[ef][1],vehicle_fleet_flag[vf])
                                        except UnboundLocalError:
                                            c_height = 1
                                    else:
                                        c_height = 1

                                    # c_speed = c_ta = c_rh = c_height = 1
                                    hef[l,h,s,vf,ft,es] = ef_equation_china.ef_equation_china(float(emission_factor[ef][6]), c_speed, c_ta, c_rh, c_height)
                                    #print(vehicle_fleet_flag[vf], speed_data[l,h], species_flag[s], fuel_type_flag[ft],emission_standard_flag[es], c_speed)

                                    total_emission[l,h,s,vf,ft,es]=hef[l,h,s,vf,ft,es] * \
                                                          flow_data[l,h] * vehicle_fleet_percentage[vehicle_fleet_flag[vf]] * \
                                                          fuel_type_percentage[vf, ft] * emission_standard_percentage[vf,es] * \
                                                          float(street_length[l]) /1000

                                    break

                ### for Bus
                for vf in range(len(vehicle_fleet_flag[0:7]),len(vehicle_fleet_flag[0:8])):
                    for ft in range(len(fuel_type_flag)):
                        if fuel_type_flag[ft] == 'LPG':
                            fuel_type_flag_bus = 'Diesel'
                        else:
                            fuel_type_flag_bus = fuel_type_flag[ft]

                        for es in range(len(emission_standard_flag)):
                            ### for evaporation
                            if species_flag[s] == 'HC' and fuel_type_flag_bus == 'Petrol':
                                total_emission[l, h, s, vf, ft, es] = total_emission[l, h, s, vf, ft, es] + (ef1 * float(street_length[l]) /1000 / speed_data[l,h] + ef2) * flow_data[l,h] \
                                                                       * vehicle_fleet_percentage[vehicle_fleet_flag[vf]] * \
                                                                      fuel_type_percentage[vf, ft] * emission_standard_percentage[vf, es]

                            for ef in range(len(emission_factor)):
                                ### for exhaust
                                if emission_factor[ef][0] == 'Buses' and emission_factor[ef][1] == fuel_type_flag_bus and \
                                        emission_factor[ef][2] == vehicle_fleet_flag_segment[vf] and emission_factor[ef][3] == emission_standard_flag[es] and \
                                        emission_factor[ef][5] == species_flag[s]:

                                    try:
                                        c_speed = ef_equation_china.speed_correction(speed_data[l,h], species_flag[s], emission_factor[ef][1], emission_standard_flag[es])
                                    except UnboundLocalError:
                                        c_speed = 1

                                    try:
                                        c_ta = ef_equation_china.ta_correction(cal_day.month, species_flag[s], emission_factor[ef][1], vehicle_fleet_flag[vf])
                                    except UnboundLocalError:
                                        c_ta = 1

                                    try:
                                        c_rh = ef_equation_china.rh_correction(cal_day.month, species_flag[s], emission_factor[ef][1])
                                    except UnboundLocalError:
                                        c_rh = 1

                                    if high_altitude:
                                        try:
                                            c_height = ef_equation_china.height_correction(species_flag[s],emission_factor[ef][1],vehicle_fleet_flag[vf])
                                        except UnboundLocalError:
                                            c_height = 1
                                    else:
                                        c_height = 1

                                    # c_speed = c_ta = c_rh = c_height = 1
                                    hef[l,h,s,vf,ft,es] = ef_equation_china.ef_equation_china(float(emission_factor[ef][6]), c_speed, c_ta, c_rh, c_height)
                                    #print(vehicle_fleet_flag[vf], speed_data[l,h], species_flag[s], fuel_type_flag[ft],emission_standard_flag[es], c_speed)

                                    ## reference S. Zhang, Y. Wu, H.liu et al, AE, 2013
                                    if fuel_type_flag[ft] == 'LPG':
                                        if species_flag[s] == 'CO':
                                            hef[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * 0.11
                                        elif species_flag[s] == 'HC':
                                            hef[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * 0.64
                                        elif species_flag[s] == 'NOx':
                                            hef[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * 1.71
                                        elif species_flag[s] == 'PM25' or species_flag[s] == 'PM10':
                                            hef[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * 0.1
                                        else:
                                            hef[l,h,s,vf,ft,es] = 0

                                    total_emission[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * \
                                                          flow_data[l,h] * vehicle_fleet_percentage[vehicle_fleet_flag[vf]] * \
                                                          fuel_type_percentage[vf, ft] * emission_standard_percentage[vf, es] * \
                                                          float(street_length[l]) /1000


                                    break


                ### for taxi
                for vf in range(len(vehicle_fleet_flag[0:8]),len(vehicle_fleet_flag[0:9])):
                    for ft in range(len(fuel_type_flag)):
                        if fuel_type_flag[ft] == 'LPG':
                            fuel_type_flag_taxi = 'Petrol'
                        else:
                            fuel_type_flag_taxi = fuel_type_flag[ft]

                        for es in range(len(emission_standard_flag)):
                            ### for evaporation
                            if species_flag[s] == 'HC' and fuel_type_flag_taxi == 'Petrol':
                                total_emission[l, h, s, vf, ft, es] = total_emission[l, h, s, vf, ft, es] + (ef1 * float(street_length[l]) /1000 / speed_data[l,h] + ef2) * flow_data[l,h] \
                                                                       * vehicle_fleet_percentage[vehicle_fleet_flag[vf]] * \
                                                                      fuel_type_percentage[vf, ft] * emission_standard_percentage[vf, es]

                            for ef in range(len(emission_factor)):
                                ### for exhaust
                                if emission_factor[ef][0] == 'Passenger Cars' and emission_factor[ef][1] == fuel_type_flag_taxi and \
                                        emission_factor[ef][2] == vehicle_fleet_flag_segment[vf] and emission_factor[ef][3] == emission_standard_flag[es] and \
                                        emission_factor[ef][5] == species_flag[s]:

                                    try:
                                        c_speed = ef_equation_china.speed_correction(speed_data[l,h], species_flag[s], emission_factor[ef][1], emission_standard_flag[es])
                                    except UnboundLocalError:
                                        c_speed = 1

                                    try:
                                        c_ta = ef_equation_china.ta_correction(cal_day.month, species_flag[s], emission_factor[ef][1], vehicle_fleet_flag[vf])
                                    except UnboundLocalError:
                                        c_ta = 1

                                    try:
                                        c_rh = ef_equation_china.rh_correction(cal_day.month, species_flag[s], emission_factor[ef][1])
                                    except UnboundLocalError:
                                        c_rh = 1

                                    if high_altitude:
                                        try:
                                            c_height = ef_equation_china.height_correction(species_flag[s],emission_factor[ef][1],vehicle_fleet_flag[vf])
                                        except UnboundLocalError:
                                            c_height = 1
                                    else:
                                        c_height = 1

                                    # c_speed = c_ta = c_rh = c_height = 1
                                    hef[l,h,s,vf,ft,es] = ef_equation_china.ef_equation_china(float(emission_factor[ef][6]), c_speed, c_ta, c_rh, c_height)
                                    #print(vehicle_fleet_flag[vf], speed_data[l,h], species_flag[s], fuel_type_flag[ft],emission_standard_flag[es], c_speed)

                                    ## reference S. Zhang, Y. Wu, H.liu et al, AE, 2013
                                    if fuel_type_flag[ft] == 'LPG':
                                        if species_flag[s] == 'CO':
                                            hef[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * 0.46
                                        elif species_flag[s] == 'HC':
                                            hef[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * 1.19
                                        elif species_flag[s] == 'NOx':
                                            hef[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * 0.75
                                        elif species_flag[s] == 'PM25' or species_flag[s] == 'PM10':
                                            hef[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * 1
                                        else:
                                            hef[l,h,s,vf,ft,es] = 0

                                    total_emission[l,h,s,vf,ft,es] = hef[l,h,s,vf,ft,es] * \
                                                          flow_data[l,h] * vehicle_fleet_percentage[vehicle_fleet_flag[vf]] * \
                                                          fuel_type_percentage[vf, ft] * emission_standard_percentage[vf, es] * \
                                                          float(street_length[l]) /1000
                                    break

    total_emission_output = np.nansum(np.nansum(np.nansum(total_emission, 5), 4), 3)

    end_time_cal = time.time()
    print('Calculation time:  %.2f s' % (end_time_cal - start_time_cal))

    ### IO part
    start_time_io=time.time()

    for s_out in range(len(species_flag)):
        save_output1 = np.savetxt(output_path + \
                                  str(cal_day.year).zfill(4) + '-' + str(cal_day.month).zfill(2) + '-' + str(
            cal_day.day).zfill(2) + '_hour_emission_' + species_flag[s_out] + '.txt', \
                                  total_emission_output[:,:,s_out], fmt='%6f', delimiter=',',
                                  header='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23', \
                                  newline='\n')

    for fuel_type_output in range(len(fuel_type_flag)):
        scio.savemat(output_path + \
                     str(cal_day.year).zfill(4) + '-' + str(cal_day.month).zfill(2) + '-' + str(
            cal_day.day).zfill(2) + '_total_emission_' + fuel_type_flag[fuel_type_output] + '.mat', \
                 {'total_emission_' + fuel_type_flag[fuel_type_output]: total_emission[:,:,:,:,fuel_type_output,:]})

    for fuel_type_output in range(len(fuel_type_flag)):
        scio.savemat(output_path + \
                     str(cal_day.year).zfill(4) + '-' + str(cal_day.month).zfill(2) + '-' + str(
            cal_day.day).zfill(2) + '_hef_' + fuel_type_flag[fuel_type_output] + '.mat', \
                 {'hef_' + fuel_type_flag[fuel_type_output]: hef[:,:,:,:,fuel_type_output,:]})

    end_time_io = time.time()

    print('IO time:  %.2f s' % (end_time_io - start_time_io))

    print('Total time:  %.2f s' % (end_time_io - start_time_cal))

