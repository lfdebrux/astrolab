#!/usr/bin/python
"""Module containing a function to convert a .csv data file in Template form into \
a .txt file readable by find_orb: Version 3- Last modified 15:41 06/11/12"""
from __future__ import division
import numpy
import csv
import sys



def convert(input_file, output_location):
    """Takes .csv file in Templated layout and returns a .txt file to output_location"""
    data = numpy.recfromcsv(input_file, delimiter=',')
    dims = data.shape
    obs_code = str(995)
    output = []
    output_filename = "C:\Users\Matt\Desktop\find_orb_positions_"
    output_filename = output_filename + str(data[0][0]) + ".txt"
    for i in xrange(dims[0]):
        i_name = data[i][0]
        i_date = data[i][1]
        i_year = i_date[0:4]
        i_year = "C"+i_year
        i_year = str(i_year)
        i_month = data[i][1][5:7]
        i_month = str(i_month)
        i_mins = data[i][2][3:5]
        i_secs = data[i][2][6:8]
        i_hours = data[i][2][0:2]
        i_day = i_date[8:10]
        
       
        i_day = float(i_day)
        
        i_hours = float(i_hours)
        i_mins = float(i_mins)
        i_secs = float(i_secs)
        i_time_decimal = (i_hours/24.0) + i_day + (i_mins/60/24) + (i_secs/60/60/24)
        
        i_time_decimal = str(i_time_decimal)
        

        
        
        
        
        
        i_RA = data[i][3]
        i_RA = str(i_RA)
        i_dec_sign = data[i][4][0]       #Obtain values
        i_dec_sign = str(i_dec_sign)
        i_dec = data[i][4][1:11]
        i_dec = str(i_dec)
        
        
        
    

        len_time = len(i_time_decimal)
        

        if i_time_decimal[1] == ".":
            i_time_decimal = "0" + i_time_decimal

        len_time = len(i_time_decimal)
        if len_time < 8:
            diff_time = 8 - len_time
            for i in range(diff_time):
                i_time_decimal = i_time_decimal + "0"

        len_time = len(i_time_decimal)
                
        if len_time > 8:
            i_time_decimal = i_time_decimal[0:8]

        

        len_RA = len(i_RA)
        if len_RA < 11:
            diff_RA = 11 - len_RA
            for i in range(diff_RA):
                i_RA = i_RA + "0"

        

        i_len = len(i_name)
        
        
        if i_len < 7:
            difference = 7 - i_len
            if difference != 0:
                for i in xrange(difference):
                    i_name = i_name + "0"
        if i_len > 7:
            i_name = i_name[0:7]

        if i_RA[-1] == " ":
            i_RA = i_RA[:-1]
        if len(i_RA) > 10:
            i_RA = i_RA[0:11]
        

        len(i_dec)
        i_string = "     "+i_name+"  "+i_year+" "+i_month+" "+i_time_decimal+" "+i_RA+" "+i_dec_sign+i_dec+"                      "+obs_code
        output.append(i_string)
    output = numpy.array(output)
    numpy.reshape(output, (1,dims[0]))
    output_filename = str(output_location) +"\Find_orb_positions_"
    output_filename = output_filename + str(data[0][0]) + ".txt"
    f = open(output_filename, "w")
    for i in range (dims[0]):
        f.write(output[i])
        f.write("\n")




if __name__ == "__main__":
    input_file = sys.argv[1]
    output_location = sys.argv[2]
    convert(input_file, output_location)

