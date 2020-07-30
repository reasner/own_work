'''
What portion of people live and work in the same county?
'''

#Import `os`
import os

# Retrieve current working directory (`cwd`)
cwd = os.getcwd()
cwd

# Change directory
os.chdir(r"/Users/mason/Documents/github_repositories/own_work")

#Import pandas & numpy
import pandas as pd
import numpy as np

input_filename = r'county_commute.csv'
cf = pd.read_csv(input_filename, engine='python')

# iterate the variable names
cf.columns = cf.columns.str.strip()
for col in cf.columns: 
    print(col)
cf = cf.drop(['county_name_res', 'county_name_wp'], axis=1)

#Own county commuters
cf['own'] = np.where((cf['state_fips_res'] == cf['state_fips_wp']) & (cf['county_fips_res'] == cf['county_fips_wp']), cf['number_commuters'], 0)
cf = cf.drop(['state_fips_wp', 'county_fips_wp'], axis=1)


#Total commuters by county
sumcf = cf.groupby(['state_fips_res', 'county_fips_res']).sum()

#Share of own county commuters
sumcf['share'] = sumcf['own']/sumcf['number_commuters']
print(sumcf.describe())

'''
In the average county 67.34% of commuters work in the same county as their residence, but there is substantial variability,
ranging from a minimum of just 9.2% and maxing out (mechanically) at 100%.
'''
