'''
Download 2000 Census County-to-County Commuting Flows:

The U.S. Census Bureau hosts the base data for the ERS commuting zones which
show flows between residence and workplace coutnies.

This file grabs the file for each state from the Census Bureau's website.
'''

#Import `os`
import os

# Retrieve current working directory (`cwd`)
cwd = os.getcwd()
cwd

# Change directory
os.chdir("/Users/mason/Documents/github_repositories/own_work")

#Import `urllib.request`

import urllib.request
census_url = r'https://www2.census.gov/programs-surveys/decennial/tables/2000/county-to-county-worker-flow-files/2kresco_us.txt'
file_name = r'county_commute.csv'

'''
states = ['ak','al','az','ca','co','ct','dc','de','fl','ga','hi','ia','id',
          'il','in','ks','ky','la','ma','md','me','mi','mn','mo','ms','mt',
          'nc','nd','ne','nh','nj','nm','nv','ny','oh','ok','or','pa','ri',
          'sc','sd','tn','tx','','','','','','',]

'''
def download_text_data(url,name):
    response = urllib.request.urlopen(url)
    raw_data = response.read()
    str_data = str(raw_data)
    observations = str_data.split(r'\n')
    observations[0] = observations[0][2:]
    nobs = len(observations)
    cleaned_obs = []
    for obs in range(nobs-1):
        state_fips_res = observations[obs][0:2]
        county_fips_res = observations[obs][3:6]
        county_name_res = observations[obs][17:58]
        state_fips_wp = observations[obs][59:61]
        county_fips_wp = observations[obs][62:65]
        county_name_wp = observations[obs][76:118]
        number_commuters = observations[obs][118:]
        new_obs = (state_fips_res + ',' + county_fips_res + ',' +
            county_name_res + ',' + state_fips_wp + ',' +
            county_fips_wp + ',' + county_name_wp + ',' +
            number_commuters)
        cleaned_obs.append(new_obs)
    return cleaned_obs,observations

output,raw_output = download_text_data(census_url, file_name)

varnames = 'state_fips_res, county_fips_res, county_name_res, state_fips_wp, county_fips_wp, county_name_wp, number_commuters'
fw = open(file_name, 'w')
fw.write(varnames + '\n')
for obs in output:
    fw.write(obs + '\n')
fw.close()




