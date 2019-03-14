#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Modified for chinese emission factor


def speed_correction(speed, species, fuel_type_flag, emission_standard_flag):

    b_speed = 1

    if fuel_type_flag == 'Petrol':
        if speed<20:
            if species == 'CO':
                b_speed = 1.69
            elif species == 'HC':
                b_speed = 1.68
            elif species == 'NOx':
                b_speed = 1.38
            elif species == 'PM25' or species == 'PM10':
                b_speed = 1.68

        if 20<=speed<30:
            if species == 'CO':
                b_speed = 1.26
            elif species == 'HC':
                b_speed = 1.25
            elif species == 'NOx':
                b_speed = 1.13
            elif species == 'PM25' or species == 'PM10':
                b_speed = 1.25

        if 30<=speed<40:
            if species == 'CO':
                b_speed = 0.79
            elif species == 'HC':
                b_speed = 0.78
            elif species == 'NOx':
                b_speed = 0.90
            elif species == 'PM25' or species == 'PM10':
                b_speed = 0.78

        if 40<=speed<80:
            if species == 'CO':
                b_speed = 0.39
            elif species == 'HC':
                b_speed = 0.32
            elif species == 'NOx':
                b_speed = 0.86
            elif species == 'PM25' or species == 'PM10':
                b_speed = 0.32

        if speed>=80:
            if species == 'CO':
                b_speed = 0.62
            elif species == 'HC':
                b_speed = 0.59
            elif species == 'NOx':
                b_speed = 0.96
            elif species == 'PM25' or species == 'PM10':
                b_speed = 0.59

    if fuel_type_flag == 'Diesel':
        if emission_standard_flag == 'CHINA IV' or emission_standard_flag == 'CHINA V':
            if speed < 20:
                if species == 'CO':
                    b_speed = 1.29
                elif species == 'HC':
                    b_speed = 1.38
                elif species == 'NOx':
                    b_speed = 1.39
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 1.36

            if 20 <= speed < 30:
                if species == 'CO':
                    b_speed = 1.10
                elif species == 'HC':
                    b_speed = 1.12
                elif species == 'NOx':
                    b_speed = 1.12
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 1.12

            if 30 <= speed < 40:
                if species == 'CO':
                    b_speed = 0.93
                elif species == 'HC':
                    b_speed = 0.91
                elif species == 'NOx':
                    b_speed = 0.91
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 0.91

            if 40 <= speed < 80:
                if species == 'CO':
                    b_speed = 0.70
                elif species == 'HC':
                    b_speed = 0.64
                elif species == 'NOx':
                    b_speed = 0.60
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 0.65

            if speed >= 80:
                if species == 'CO':
                    b_speed = 0.61
                elif species == 'HC':
                    b_speed = 0.48
                elif species == 'NOx':
                    b_speed = 0.28
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 0.48
        else:
            if speed < 20:
                if species == 'CO':
                    b_speed = 1.43
                elif species == 'HC':
                    b_speed = 1.41
                elif species == 'NOx':
                    b_speed = 1.31
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 1.22

            if 20 <= speed < 30:
                if species == 'CO':
                    b_speed = 1.14
                elif species == 'HC':
                    b_speed = 1.13
                elif species == 'NOx':
                    b_speed = 1.08
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 1.08

            if 30 <= speed < 40:
                if species == 'CO':
                    b_speed = 0.89
                elif species == 'HC':
                    b_speed = 0.90
                elif species == 'NOx':
                    b_speed = 0.93
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 0.93

            if 40 <= speed < 80:
                if species == 'CO':
                    b_speed = 0.54
                elif species == 'HC':
                    b_speed = 0.61
                elif species == 'NOx':
                    b_speed = 0.74
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 0.71

            if speed >= 80:
                if species == 'CO':
                    b_speed = 0.61
                elif species == 'HC':
                    b_speed = 0.41
                elif species == 'NOx':
                    b_speed = 0.66
                elif species == 'PM25' or species == 'PM10':
                    b_speed = 0.49

    return b_speed


def ta_correction(month, species, fuel_type_flag, vehicle_fleet_flag):

    b_ta = 1
    if fuel_type_flag == 'Petrol':
        if 5 < month <= 10:
            if species == 'CO':
                b_ta = 1.23
            if species == 'HC':
                b_ta = 1.08
            if species == 'NOx':
                b_ta = 1.31

        if month < -1:    ### in Guangzhou, there is hadly temperature below 10
            if species == 'CO':
                b_ta = 1.36
            if species == 'HC':
                b_ta = 1.47
            if species == 'NOx':
                b_ta = 1.15

    if fuel_type_flag == 'Diesel':
        if 5 < month <= 10:
            if vehicle_fleet_flag == 'LDV':
                if species == 'CO':
                    b_ta = 1.33
                if species == 'HC':
                    b_ta = 1.07
                if species == 'NOx':
                    b_ta = 1.17
                if species == 'PM25' or species == 'PM10':
                    b_ta = 0.68
            elif vehicle_fleet_flag == 'LDT':
                if species == 'CO':
                    b_ta = 1.33
                if species == 'HC':
                    b_ta = 1.06
                if species == 'NOx':
                    b_ta = 1.17
                if species == 'PM25' or species == 'PM10':
                    b_ta = 0.90
            else:
                if species == 'CO':
                    b_ta = 1.30
                if species == 'HC':
                    b_ta = 1.06
                if species == 'NOx':
                    b_ta = 1.15
                if species == 'PM25' or species == 'PM10':
                    b_ta = 0.74

        if month < -1: ### in Guangzhou, there is hadly temperature below 10
            if vehicle_fleet_flag == 'LDV':
                if species == 'CO':
                    b_ta = 1
                if species == 'HC':
                    b_ta = 1
                if species == 'NOx':
                    b_ta = 1.06
                if species == 'PM25' or species == 'PM10':
                    b_ta = 1.87
            elif vehicle_fleet_flag == 'LDT':
                if species == 'CO':
                    b_ta = 1
                if species == 'HC':
                    b_ta = 1
                if species == 'NOx':
                    b_ta = 1.05
                if species == 'PM25' or species == 'PM10':
                    b_ta = 1.27
            else:
                if species == 'CO':
                    b_ta = 1
                if species == 'HC':
                    b_ta = 1
                if species == 'NOx':
                    b_ta = 1.06
                if species == 'PM25' or species == 'PM10':
                    b_ta = 1.7

    return b_ta


def rh_correction(month, species, fuel_type_flag):

    b_rh = 1

    if fuel_type_flag == 'Petrol':
        if 5 < month <= 10:
            if month > 0:           ###in Guangzhou, no month rh is below 50%
                if species == 'CO':
                    b_rh = 1.04
                if species == 'HC':
                    b_rh = 1.01
                if species == 'NOx':
                    b_rh = 0.87

            if month < -1:          ###in Guangzhou, no month rh is below 50%
                if species == 'CO':
                    b_rh = 0.97
                if species == 'HC':
                    b_rh = 0.99
                if species == 'NOx':
                    b_rh = 1.13
        else:
            if month > 0:           ###in Guangzhou, no month rh is below 50%
                if species == 'NOx':
                    b_rh = 0.92

            if month < -1:          ###in Guangzhou, no month rh is below 50%
                if species == 'NOx':
                    b_rh = 1.06

    if fuel_type_flag == 'Diesel':
        if 5 < month <= 10:
            if month > 0:  ###in Guangzhou, no month rh is below 50%
                if species == 'NOx':
                    b_rh = 0.88
            if month < -1:  ###in Guangzhou, no month rh is below 50%
                if species == 'NOx':
                    b_rh = 1.12
        else:
            if month > 0:  ###in Guangzhou, no month rh is below 50%
                if species == 'NOx':
                    b_rh = 0.94

            if month < -1:  ###in Guangzhou, no month rh is below 50%
                if species == 'NOx':
                    b_rh = 1.04

    return b_rh


def height_correction(species, fuel_type_flag, vehicle_fleet_flag):

    b_height = 1

    if vehicle_fleet_flag == 'LDV' or vehicle_fleet_flag == 'LDT' or vehicle_fleet_flag == 'Taxi':
        if fuel_type_flag != 'Diesel':
            if species == 'CO':
                b_height = 1.58
            if species == 'HC':
                b_height = 2.46
            if species == 'NOx':
                b_height = 3.15

    if vehicle_fleet_flag == 'LDV' or vehicle_fleet_flag == 'LDT':
        if fuel_type_flag == 'Diesel':
            if species == 'CO':
                b_height = 1.2
            if species == 'HC':
                b_height = 1.32
            if species == 'NOx':
                b_height = 1.35

    if vehicle_fleet_flag == 'MDV' or vehicle_fleet_flag == 'MDT' or vehicle_fleet_flag == 'LDV' or vehicle_fleet_flag == 'LDT' or vehicle_fleet_flag == 'Bus':
        if fuel_type_flag != 'Diesel':
            if species == 'CO':
                b_height = 3.95
            if species == 'HC':
                b_height = 2.26
            if species == 'NOx':
                b_height = 0.88

    if vehicle_fleet_flag == 'MDV' or vehicle_fleet_flag == 'MDT' or vehicle_fleet_flag == 'LDV' or vehicle_fleet_flag == 'LDT' or vehicle_fleet_flag == 'Bus':
        if fuel_type_flag == 'Diesel':
            if species == 'CO':
                b_height = 2.46
            if species == 'HC':
                b_height = 2.05
            if species == 'NOx':
                b_height = 1.02

    return b_height


def ef_equation_china(ef, b_speed, b_ta, b_rh, b_height):

    hef = ef * b_speed * b_ta * b_rh * b_height

    return hef
