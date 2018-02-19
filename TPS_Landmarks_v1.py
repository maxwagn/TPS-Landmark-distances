# !/usr/bin/env python
# written by Maximilian Wagner

import math
import sys
import itertools

sys.stdout.write('''
   # Automatically calculates Truss-distances between landmarks of TPS-file.
   # Returns csv-file with distances of given Landmark configurations:
   # Example-template for metafile:
        (1, 2); SL
        (4, 1); Interorbital distance
        (8, 2); HW
    
   # usage: $ python TPS_Landmarks_v1.py TPS_input_name.TPS outfile_name.csv metafile_name.txt

    ''')

TPS_file_name = sys.argv[1]
out_file_name = sys.argv[2]
metadata = sys.argv[3]

def parsing_TPS(TPSfile):
    "Parses TPS-Inputfile and returns a dictionary"
    read_coords = False
    parsed_dict = {}
    with open(TPSfile) as fh:
        for line in fh:
            line = line.rstrip()
            if line.startswith("LM"):
                list_x = []
                list_y = []
                sample_list = []
                read_coords = True
                continue
            if line.startswith("IMAGE"):
                read_coords = False
                sample_list.append(line.replace("IMAGE=", ""))
            if read_coords:
                list_x.append(float(line.split()[0]))
                list_y.append(float(line.split()[1]))
                continue
            if line.startswith("SCALE"):
                sample_list.append(float(line.replace("SCALE=","")))
                sample_list.extend([list_x, list_y])
                parsed_dict[sample_list[0]]=sample_list[1:]
    return parsed_dict

def _distance1(ID,xcoordinates,ycoordinates,Scale):
    '''Calculates Euclidian distances between two landmarks and corrects for Scale factor (set in TPS file).
    Returns distances for every specimen in an dictionary'''
    distance_list = []
    distance_dict = {}
    listx = []
    listy = []
    LM_combinations = list(itertools.permutations(range(1, LMs + 1), r=2))
    for i in xcoordinates:
        for j in xcoordinates:
            listx.append((i-j)**2)
    for i in ycoordinates:
        for j in ycoordinates:
            listy.append((i-j)**2)
    distance = []
    for a, b in zip(listx, listy):
        d = math.sqrt(a+b) * Scale
        distance.append(d)
    for value in distance:
        if value > 0:
            distance_list.append(value)
    distance_dict[ID] = {}
    for i in range(len(LM_combinations)):
        distance_dict[ID][str(LM_combinations[i])]=distance_list[i]
    return (distance_dict)

def number_of_LMs(TPSfile):
    "Returns number of Landmarks in the dataset."
    with open(TPSfile) as fh:
        first_line_read = fh.readline()
        first_line = first_line_read.replace("LM=", "")
        No_of_LM = int(first_line)
    return No_of_LM

working_data = parsing_TPS(TPS_file_name)
LMs = number_of_LMs(TPS_file_name)

sample = []
for key, value in working_data.items():
    ID = key
    xcor = value [1]
    ycor = value [2]
    scale = value [0]
    sample.append(_distance1(ID,xcor,ycor,scale))

metadict = dict()
with open(metadata) as meta:
    for line in meta:
        line = line.rstrip()
        lm_meta = str()
        measures = str()
        lm_meta += line.split(";")[0]
        measures += line.split(";")[1]
        for i in lm_meta:
            for j in measures:
                metadict[str(lm_meta)]=str(measures)

text = str()
heading = str('ID, ')
counter = 1
for dictionary in sample:
    for ID, sample_dict in dictionary.items():
        text += '\n' + ID + ", "
        for from_to in sample_dict:
            if from_to in metadict:
                if counter <= 3:
                    heading += metadict[from_to] + ", "
                    text += str(sample_dict[from_to]) + ", "
                    counter += 1
                else:
                    text += str(sample_dict[from_to]) + ", "


outputfile = open(out_file_name, "w")
outputfile.write(heading[:-2] + '\n' + text[1:])

print("\nName of TPS-file: {}".format(TPS_file_name))
print("Name of Metadata_file: {}".format(metadata))
print("Name of output-file: {}".format(out_file_name))
print("Number of Landmarks in your dataset: {}".format(LMs))
