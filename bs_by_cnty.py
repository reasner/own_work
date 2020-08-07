'''
Transform All Banks by Year into All Banks by County
'''

import os
import csv

#define years
years = []
for add in range(25):
    years.append(str(1995+add))
                 
#make storage directory
parent = r'/Users/mason/Documents/phd/research/bank_comp/bank_deposit_survey/orig_csv/'
stor_dir = "FIPS"
stor_path = os.path.join(parent, stor_dir)
if not os.path.exists(stor_path):
    os.mkdir(stor_path)
data_by_county = {}

#change directory to working
for year in years:
    data_path = r'ALL_' + year
    path = os.path.join(parent, data_path) 
    os.chdir(path)
    print("Current Working Directory " , os.getcwd())
    filename = r'ALL_' + year + r'.csv'

    fields = [] 
    rows = []
    # reading csv file 
    with open(filename, 'r', encoding='ISO-8859-1') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
          
        # extracting field names through first row 
        fields = next(csvreader) 
      
        # extracting each data row one by one 
        for row in csvreader: 
            rows.append(row)
    nobs = len(rows)
    extract_fips = []
    for i in range(nobs):
            extract_fips.append(str(rows[i][36]).zfill(5))
    unique_fips = set(extract_fips)
    
    data_by_county[year] = {}
    for fips in unique_fips:
        os.chdir(stor_path)
        temp_data = []
        for i,j in enumerate(extract_fips):
            if j == fips:
                if rows[i][32] != '' and rows[i][33] != '' and rows[i][3] != '':
                    temp_data.append(rows[i])
        data_by_county[year][fips] = temp_data
        new_file_name = r'fips_' + fips + r'.csv'
        if year == '1995':
            with open(new_file_name, mode='w') as bank_file:
                bank_writer = csv.writer(bank_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                bank_writer.writerow(fields)
                for data_point in data_by_county[year][fips]:
                    bank_writer.writerow(data_point)
        else:
            with open(new_file_name, 'a+', newline='') as bank_file:
                bank_writer = csv.writer(bank_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for data_point in data_by_county[year][fips]:
                    bank_writer.writerow(data_point)

list_file_name = r'unique_fips.csv'
with open(list_file_name, mode='w') as fips_file:
    fips_writer = csv.writer(fips_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for fips in unique_fips:
        temp_list = [fips]
        fips_writer.writerow(temp_list)
        
