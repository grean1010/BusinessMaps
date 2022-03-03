#######################################################################################
## Title:   03_Add_Data2Geojson.py
## Author:  Maria Cupples Hudson
## Purpose: Take cleaned BDS data and add to geojson files for each year
## Updates: 03/02/2022 Adapted previous code for BDS
#######################################################################################
##
##
#######################################################################################
import pandas as pd
import json
import csv 
import os

# location of this folder on the hard drive
base_loc = os.path.join('C:\\','Users','laslo','OneDrive','Documents','Maria','BusinessMaps')

# Set locations for raw and clean data folders.
raw_loc = os.path.join(base_loc,'RawData')
clean_loc = os.path.join(base_loc,'CleanData')

map_html = os.path.join(base_loc,'map_html')
map_png = os.path.join(base_loc,'map_png')

#######################################################################################
## Import clean data by county and date
#######################################################################################

# Read the cleaned case/death data into a dataframe
indata = os.path.join(clean_loc,'bds_clean.csv')
cleandata = pd.read_csv(indata)

# Create functions to add leading zeros to 5 digit codes
def make5d(x):
    if len(str(x)) == 4:
        x2 = f'0{x}'
    else:
        x2 = f'{x}'
    return x2

# Add leading zeros to state and county codes. Set together to create FIPS.
cleandata['FIPS']=cleandata['FIPS'].apply(make5d)

# Make sure FIPS is the first column
cols_reorder = cleandata.columns.to_list()
cols_reorder.remove('FIPS')
cols_reorder.insert(0,'FIPS')
cleandata = cleandata[cols_reorder]

print ("First 5 rows of the cleandata dataframe")
print(cleandata.head(5))

#######################################################################################
## Create a function to create a geojson file for each each point in time with all of
## the data we will use to create maps for that particular date.
#######################################################################################
def make_geofile(timepoint):

    # Set the name of the input and output geojson file. Note that these are the 
    # same because we assume that the 02b program has already been run.
    json_input = os.path.join(clean_loc,f'InitialGeoFile{timepoint}.json')
    json_output = os.path.join(clean_loc,f'FinalGeoFile{timepoint}.json')

    # pull the year from the date variable
    y = int(timepoint[0:4])

    ratedata4timepoint = {}
        
    # Loop through the dataframe and add information to the data2add dictionary. 
    # We will use this to put these values into the geojson.
    for row, rowvals in cleandata.iterrows():
        
        # pull the fips code from the first entry in the row
        FIPS = rowvals[0]
    
        # If we have not previously seen this fips code, add it to the dictionary
        if FIPS not in ratedata4timepoint:
            ratedata4timepoint[FIPS]={}
            
        # pull county name, state abbreviation and all other info for this timepoint
        ratedata4timepoint[FIPS]['job_creation_rate'] = rowvals[cols_reorder.index(f'job_creation_rate_{y}')]  


    # Add the data we will be mapping to the json file
    # Create a blank geojson that we will build up with the existing one plus the new information
    geojson = {}
    
    # Open up the existing geojson file and read it into the empty geojson dictionary created above.
    # While reading it in, pull the matching fips from the data2add dictionary so we can add the
    # variable as a feature/property in the geojson.
    with open(json_input, 'r') as f:
        geojson = json.load(f)
        for feature in geojson['features']:
            featureProperties = feature['properties']
            FIPS = featureProperties['FIPS']

            featureData = ratedata4timepoint.get(FIPS, {})
            for key in featureData.keys():
                featureProperties[key] = featureData[key]
                
    # Output this updated geojson.
    with open(json_output, 'w') as f:
        json.dump(geojson, f)

    print(f"Creating final geojson file for {timepoint}. Output file name: {json_output}.")

# Run each date for which we have clean data
for yyyy in range(1978,2020):
    print(f'Starting to create output for year {yyyy}.')
    make_geofile(f'{yyyy}0101')
