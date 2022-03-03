#######################################################################################
## Title:   02_Clean_Data.py
## Author:  Maria Cupples Hudson
## Purpose: Read BDS data downloaded from Census. These files are at the year-county
##          contain multiple measures of business activity. We focus on job creation
##          rates. Ultimately we want a county-level file with the job creation rate
##          for each year.
##
## Updates: 03/02/2022 Code Written
##
#######################################################################################
##
##
#######################################################################################
import pandas as pd
import os

base_loc = os.path.join('C:\\','Users','laslo','OneDrive','Documents','Maria','BusinessMaps')
raw_loc = os.path.join(base_loc,'RawData')
clean_loc = os.path.join(base_loc,'CleanData')

# Read BDS data into a dataframe
bdsdata = os.path.join(raw_loc,'bds2019_cty.csv')
bds = pd.read_csv(bdsdata)


print("First 5 observations in raw dataframe:")
print(bds.head())

# Create functions to add leading zeros to 2/3 digit codes
def make2d(x):
    if len(str(x)) == 0:
        x = f'00'
    elif len(str(x)) == 1:
        x = f'0{x}'
    return x

def make3d(x):
    if len(str(x)) == 0:
        x = f'000'
    elif len(str(x)) == 1:
        x = f'00{x}'
    elif len(str(x)) == 2:
        x = f'0{x}'
    return x
        
# Add leading zeros to state and county codes. Set together to create FIPS.
bds['STATEFP']=bds['st'].apply(make2d)
bds['COUNTYFP']=bds['cty'].apply(make3d)
bds['FIPS']=bds.apply(lambda x:'%s%s' % (x['STATEFP'],x['COUNTYFP']),axis=1)


years_in_data = bds['year'].unique()
print('These are the years we see in the BDS dataframe')
print(years_in_data)

counties_in_data = bds['FIPS'].unique()
print('These are the counties we see in the BDS dataframe')
print(counties_in_data)

# Build the clean dataset by starting with the distinct counties.
bds_clean = pd.DataFrame(counties_in_data)
bds_clean=bds_clean.rename(columns={bds_clean.columns[0]: 'FIPS'})

# The rates are often stored as character. Create a funtion to convert to float.
def convert2float(x):
    try:
        x2 = float(x)
    except:
        x2 = None
    return x2

# Loop through the years in the data to create year-specific variables and add on to clean data.
for y in years_in_data:
    
    # Pull the year and month from the timepoint 
    print(f'Adding data for year = {y}')
    
    tempds = bds.loc[(bds["year"] == y), ['FIPS','job_creation_rate']]

    print(f'We found {len(tempds)} records for year {y}.')
    
    tempds[f'job_creation_rate_{y}']=tempds['job_creation_rate'].apply(convert2float)
    tempds = tempds.drop(['job_creation_rate'], axis=1)
    
    bds_clean = pd.merge(bds_clean,tempds,on=['FIPS'],how='outer')

# Output to csv
bds_clean.to_csv(os.path.join(clean_loc,'bds_clean.csv'))


print("First 5 observations in clean dataframe:")
print(bds_clean.head())

# Find absolute min/max of the job creation rates. We will use these later to inform graph colors.
rates_in_data = bds['job_creation_rate'].unique()
print(f'Rates in data: {rates_in_data}')
current_max = 0
current_min = 100

for r in rates_in_data:
    try:
        r2 = float(r)
        if r2 > current_max:
            current_max = r2
        if r2 < current_min:
            current_min = r2
        #print(f'Converting {r} to float: {r}. Current max {current_max}. Current min {current_min}')

    except:
        print(f'Non-numeric value {r} for rate. Disregard.')

print(f'Absolute max job creation rate is {current_max}. Min is {current_min}.')
print('Use these to inform color choices for maps in later programs.')