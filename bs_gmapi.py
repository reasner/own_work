'''
Take Bank Survey Data, Request within county distances for all banks
in each year from google maps distance matrix api, and save them
'''

#Import packages
import os
import csv 
import itertools
import math
import urllib.request
import json

#Define functions
### Great Circle Distance #1: Spherical Law of Cosines
def gc1_sloc(coordinate_1,coordinate_2,radius):
    lon1,lat1 = coordinate_1
    lon2,lat2 = coordinate_2
    lonrat1 = lon1/(180/math.pi)
    lonrat2 = lon2/(180/math.pi)
    latrat1 = lat1/(180/math.pi)
    latrat2 = lat2/(180/math.pi)
    difflonrat = lonrat1-lonrat2
    difflatrat = latrat1-latrat2
    inner_cent_ang = math.sin(latrat1)*math.sin(latrat2) + math.cos(latrat1)*math.cos(latrat2)*math.cos(difflonrat)
    cent_ang = math.acos(inner_cent_ang)
    dist_sloc = radius*cent_ang
    return round(dist_sloc,2)

### Great Circle Distance #2: Haversine Formula
def gc2_hf(coordinate_1,coordinate_2,radius):
    lon1,lat1 = coord1
    lon2,lat2 = coord2
    lonrat1 = lon1/(180/math.pi)
    lonrat2 = lon2/(180/math.pi)
    latrat1 = lat1/(180/math.pi)
    latrat2 = lat2/(180/math.pi)
    difflonrat = lonrat1-lonrat2
    difflatrat = latrat1-latrat2
    inner_cent_ang = math.sqrt((math.sin(difflatrat/2)**2)+math.cos(latrat1)*math.cos(latrat2)*(math.sin(difflonrat/2)**2))
    cent_ang = 2*math.asin(inner_cent_ang)
    dist_hav = radius*cent_ang
    return round(dist_hav,2)

#Split list into chunks of size n
def chunk(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

#Function to get API key (sensitive data)
def getgoogleapikey(api_filename):
    api_object  = open(api_filename, 'r')
    my_api = api_object.read()
    api_object.close()
    return my_api

#get API key
api_file = r'google_api_key.txt'
api_key = getgoogleapikey(api_file)

#change directory to working
parent = r'/Users/mason/Documents/phd/research/bank_comp/bank_deposit_survey/orig_csv/'
stor_dir = "FIPS"
path = os.path.join(parent, stor_dir) 
os.chdir(path)
print("Current Working Directory " , os.getcwd())


#load unique fips
fips_file_name = r'unique_fips.csv'
with open(fips_file_name, mode='r') as fips_file:
    fips_reader = csv.reader(fips_file) 
    unique_fips = []
    for row in fips_reader: 
        unique_fips.append(row[0])

for fips in unique_fips:
    temp_file_name = r'fips_' + fips + r'.csv'
    with open(temp_file_name, 'r', encoding='ISO-8859-1') as temp_file:
        tempreader = csv.reader(temp_file)
        fields = next(tempreader)
        fields = [] 
        rows = []
        for row in tempreader: 
            rows.append(row)
             
    #Work with columns
    nobs = len(rows)
    extract_unid = []
    extract_lon = []
    extract_lat = []
    for i in range(nobs):
            extract_unid.append(rows[i][3])
            extract_lat.append(rows[i][32])
            extract_lon.append(rows[i][33])
    unique_wn_unid = set(extract_unid)

    #Data structure with bank id and lon./lat. by county
    loc_by_unid = {}

    for unid in unique_wn_unid:
        temp_lon = 0
        temp_lat = 0
        for i,j in enumerate(extract_unid):
            if j == unid and temp_lon == 0 and temp_lat == 0:
                loc_by_unid[unid] = [extract_lon[i],extract_lat[i]]

    #All combinations with county of bankid
    unid_comb = list(itertools.product(unique_wn_unid,repeat=2))

    #Distance between all banks within a county (great circle)
    fips_unid_comb_w_dist = {}
    fips_list = []
    for pair in unid_comb:
        lon1 = float(loc_by_unid[pair[0]][0])
        lat1 = float(loc_by_unid[pair[0]][1])
        lon2 = float(loc_by_unid[pair[1]][0])
        lat2 = float(loc_by_unid[pair[1]][1])
        coord1 = lon1,lat1
        coord2 = lon2,lat2
        wgs_mer = 6371000
        if coord1 != coord2:
            dist1 = gc1_sloc(coord1,coord2,wgs_mer)
            dist2 = gc2_hf(coord1,coord2,wgs_mer)
        if coord1 == coord2:
            dist1 = 0
            dist2 = 0
        pair_list = [pair[0],pair[1],dist1,dist2]
        fips_list.append(pair_list)
    fips_unid_comb_w_dist[fips] = fips_list
print(fips_unid_comb_w_dist)
'''   

with open('all_bank_dist.csv', mode='w') as dist_file:
    dist_writer = csv.writer(dist_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dist_writer.writerow(['FIPS', 'UNID1', 'UNID2', 'DIST_SLOC', 'DIST_HF'])
    for fips in unique_wn_fips:
        temp_len = len(fips_unid_comb_w_dist[fips])
        for i in range(temp_len):
            dist_writer.writerow([fips] + fips_unid_comb_w_dist[fips][i])


#Distance between all banks within a county (google maps)
fips_unid_comb_w_idist = {}
fips = '01001'
fips_pair_num = len(fips_unid_comb[fips])
fips_list = []
url_snippet = r'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric'
orig_str_snippet = r'origins='
dest_str_snippet = r'destinations='
dest_list = []
key_str = r'key=' + api_key
fips_dist = {}

for orig in unid_by_county[fips][0]:
    orig_dist = {}
    orig_index = unid_by_county[fips][0].index(orig)
    orig_lon = unid_by_county[fips][1][orig_index]
    orig_lat = unid_by_county[fips][2][orig_index]
    orig_str = orig_str_snippet + str(orig_lat) + r'%2c' + str(orig_lon)

    urls_to_use = []
    for dest_chunk in chunk(unid_by_county[fips][0],4):
        dest_list = []
        for dest in dest_chunk:
            dest_index = unid_by_county[fips][0].index(dest)
            dest_lon = unid_by_county[fips][1][dest_index]
            dest_lat = unid_by_county[fips][2][dest_index]
            dest_temp = str(dest_lat) + r'%2c' + str(dest_lon)
            dest_list.append(dest_temp)
        dest_list_str = '%7C'.join(dest_list)
        dest_str = dest_str_snippet + dest_list_str
        url_to_use = url_snippet + '&' + orig_str + "&" + dest_str + '&' + key_str[:-2]
        response = urllib.request.urlopen(url_to_use)
        uncleaned_data = response.read()
        encoding = response.info().get_content_charset('utf-8')
        JSON_object = json.loads(uncleaned_data.decode(encoding))
        for num,dest in enumerate(dest_chunk):
            curr_dest = dest_chunk[num]
            orig_dist[curr_dest] = JSON_object['rows'][0]['elements'][num]['distance']['value']
        break
    fips_dist[orig] = orig_dist




look up bank id 453769 to 480332 (4.620km) versus 480332 to 453769 (5.311km)

make sure this is all the origins, for each these, I have the first 4 as dest which makes sense given the break in the chunking loop
'453769','252432','480332','011936','418434','467756','220634','479786','001806','009649','233673','500234','442218','497949','444616','531913'

make sure test.txt (addresses) aligns correctly with unid in
'531913': {'453769': 2891, '252432': 3761, '480332': 2333, '011936': 1982}}
(last dict addition to fips_dist



#For Google APIS
# %20 is space in url encoding
# %2C is comma in url encoding
# %7C is pipe in url encoding
# URLs limited to 8192 characters

#Test Coordinates
lon1 = -0.116773
lat1 = 51.510357
lon2 = -77.009003
lat2 = 38.889931

coord1 = [lon1,lat1]
coord2 = [lon2,lat2]

a = gc1_sloc(coord1,coord2,wgs_mer)
b = gc2_hf(coord1,coord2,wgs_mer)
print(a)
print(b)



#JSON in Python
#https://realpython.com/python-json/

#Distance Matrix API
#https://developers.google.com/maps/documentation/distance-matrix/start
'''


