'''
Clean up many .tex regression output tables for Serbian Trade Project
'''

import os
import string

table_path= r'/Users/mason/Dropbox/current_projects/stp/output/reg_tables'

#Current working directory
pycwd = os.getcwd()

#Change to folder w/ regression tables
os.chdir(table_path)

#Did change work
newcwd = os.getcwd()

allitems = os.listdir()

imp_reg_tables = []
exp_reg_tables = []

#Collects Export Tables
for item in allitems:
    if item[:9] == 'exp_dist_':
        exp_reg_tables.append(item)

#Collect Import Tables
for item in allitems:
    if item[:9] == 'imp_dist_':
        imp_reg_tables.append(item)

#Open Export Tables and Change Title
for item in exp_reg_tables:
    item_name = item[14:-4]
    item_name_space = item_name.replace('_',' ')
    item_title = string.capwords(item_name_space)  
    fr = open(item, 'r')
    read_data = fr.read()
    new_data = read_data.replace(r"caption{Export Entry and Learning from Neighbors [All Firms/By Industry Signal]",
        r"caption{Export Entry and Learning from Neighbors [" + item_title + "]")
    fr.close()

    fw = open(item, 'w')
    fw.write(new_data)
    fw.close() 

#Open Import Tables and Change Title
for item in imp_reg_tables:
    item_name = item[14:-4]
    item_name_space = item_name.replace('_',' ')
    item_title = string.capwords(item_name_space)
        
    fr = open(item, 'r')
    read_data = fr.read()
    new_data = read_data.replace(r"caption{Import Entry and Learning from Neighbors [All Firms/By Industry Signal]",
        r"caption{Import Entry and Learning from Neighbors [" + item_title + "]")
    fr.close()

    fw = open(item, 'w')
    fw.write(new_data)
    fw.close()
