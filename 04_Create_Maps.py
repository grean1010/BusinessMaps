#######################################################################################
## Title:   04_Create_Maps.py
## Author:  Maria Cupples Hudson
## Purpose: Take geojson files and create maps of job creation raates for each year
## Updates: 10/14/2019 Code Written
##          06/03/2020 Updated to work with Coronavirus data
##          03/02/2022 Updated to work with BDS data
#######################################################################################
##
##
#######################################################################################
import folium
import pandas as pd
import os
import datetime

# location of this folder on the hard drive
base_loc = os.path.join('C:\\','Users','laslo','OneDrive','Documents','Maria','BusinessMaps')

# Set locations for raw and clean data folders.
raw_loc = os.path.join(base_loc,'RawData')
clean_loc = os.path.join(base_loc,'CleanData')

map_html = os.path.join(base_loc,'map_html')
map_png = os.path.join(base_loc,'map_png')

#######################################################################################
## Create a function to set county color based on value
#######################################################################################

def covid_colors(feature,var2map):
    
    try: 
        test_value = feature['properties'][f'{var2map}']
    except:
        test_value = -1
        
    #print(f'var2map = {var2map}   test_value = {test_value}')
    
    # Set the delineation for the color scheme to be used in the map
    if var2map == 'Cases':
        color_list = case_colors
    elif var2map == 'Deaths':
        color_list = death_colors
    elif var2map == 'NewCasesPer100K':
        color_list = cp100k_colors
    elif var2map == 'NewDeathsPer100K':
        color_list = dp100k_colors
    elif var2map == 'Pct_Vaxxed':
        color_list = pvax_colors
    elif var2map == 'AveTemp':
        color_list = temp_colors
    elif var2map == 'job_creation_rate':
        color_list = jcr_colors

    """Maps low values to green and high values to red."""
    if test_value > color_list[9]:
        return f'{scale2use[9]}'
    elif test_value > color_list[8]:
        return f'{scale2use[8]}'
    elif test_value > color_list[7]:
        return f'{scale2use[7]}'
    elif test_value > color_list[6]:
        return f'{scale2use[6]}'
    elif test_value > color_list[5]:
        return f'{scale2use[5]}'
    elif test_value > color_list[4]:
        return f'{scale2use[4]}'
    elif test_value > color_list[3]:
        return f'{scale2use[3]}'
    elif test_value > color_list[2]:
        return f'{scale2use[2]}'
    elif test_value > color_list[1]:
        return f'{scale2use[1]}'
    elif test_value > color_list[0]:
        return f'{scale2use[0]}'
    else:
        return "#lightgray"


#######################################################################################
## Create a function to create a the html file containing maps with all of the 
## information in the tooltip and colored by the specified feature.
#######################################################################################
def make_map(timepoint,SaveName,var2map):
    
    # pull the year from the date variable
    year2check = int(timepoint[0:4])

    # Note the file locations of input/output json, html, and png files
    json_input = os.path.join(clean_loc,f'FinalGeoFile{timepoint}.json')
    json_output = os.path.join(clean_loc,f'FinalGeoFile{timepoint}.json')
    save_html = os.path.join(map_html,f'{SaveName}_{timepoint}.html')
    save_png = os.path.join(map_png,f'{SaveName}_{timepoint}.png')
    
    # Pull the year and month from the timepoint 
    yearpoint = timepoint[0:4]
    monthpoint = datetime.date(int(timepoint[0:4]), int(timepoint[4:6]), int(timepoint[6:8])).strftime('%B')
    daynum = timepoint[6:8]
    mdy = f"{timepoint[0:4]}/{timepoint[4:6]}/{timepoint[6:8]}"

    # Create a list of fields to be included in the tooltip and a list of descriptions for those variables
    # Use the name of the variable to determine the tooltip list contents
    tip_fields = ['FIPS','job_creation_rate']
    tip_aliases = ['FIPS:','Job Creation Rate:']
    
    
    # Set the color scheme to be used in the map
    if var2map == 'Cases':
        color_list = case_colors
    elif var2map == 'Deaths':
        color_list = death_colors
    elif var2map == 'NewCasesPer100K':
        color_list = cp100k_colors
    elif var2map == 'NewDeathsPer100K':
        color_list = dp100k_colors
    elif var2map == 'Pct_Vaxxed':
        color_list = pvax_colors
    elif var2map == 'AveTemp':
        color_list = temp_colors
    elif var2map == 'job_creation_rate':
        color_list = jcr_colors
  
    #print(color_list)
    
   
    m = folium.Map([43,-100], tiles='cartodbpositron', zoom_start=4.25)

    # Display the month on the top of the page
    title_html = f'''
        <div style="position: fixed; 
                 bottom: 90%;
                 right: 50%;
                 align: center;
                 z-index: 1001;
                 padding: 6px 8px;
                 font: 40px Arial, Helvetica, sans-serif;
                 font-weight: bold;
                 line-height: 18px;
                 color: 'black';">
        <h3><b><center><br>Job Creation Rate <br>{yearpoint} </center></b></h3></div>'''

    m.get_root().html.add_child(folium.Element(title_html))

    # Create legend text
    legend_html = f'''
         <div style="position: fixed; 
                     bottom: 5%;
                     right: 5%;
                     z-index: 1000;
                     padding: 6px 8px;
                     width: 120px;
                     font: 12px Arial, Helvetica, sans-serif;
                     font-weight: bold;
                     background: #8d8a8d;
                     border-radius: 5px;
                     box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
                     line-height: 18px;
                     color: 'black';">


         <i style="background: {scale2use[9]}"> &nbsp &nbsp</i> {color_list[9]}+ <br>
         <i style="background: {scale2use[8]}" > &nbsp &nbsp</i> {color_list[8]} - {color_list[9]}<br>
         <i style="background: {scale2use[7]}"> &nbsp &nbsp</i> {color_list[7]} - {color_list[8]}<br>
         <i style="background: {scale2use[6]}"> &nbsp &nbsp</i> {color_list[6]} - {color_list[7]}<br>
         <i style="background: {scale2use[5]}"> &nbsp &nbsp</i> {color_list[5]} - {color_list[6]}<br>
         <i style="background: {scale2use[4]}"> &nbsp &nbsp</i> {color_list[4]} - {color_list[5]}<br>
         <i style="background: {scale2use[3]}"> &nbsp &nbsp</i> {color_list[3]} - {color_list[4]}<br>
         <i style="background: {scale2use[2]}"> &nbsp &nbsp</i> {color_list[2]} - {color_list[3]}<br>
         <i style="background: {scale2use[1]}"> &nbsp &nbsp</i> {color_list[1]} - {color_list[2]}<br>
         <i style="background: {scale2use[0]}"> &nbsp &nbsp</i> 0<br>
          </div>
         '''

    
    # Add the legend to the html
    m.get_root().html.add_child(folium.Element(legend_html))

    folium.GeoJson(json_output,
                   style_function=lambda feature: {
                                            'fillColor': covid_colors(feature,f"{var2map}"),
                                            'fillOpacity' : '0.8',
                                            'color' : 'black',
                                            'weight' : 0
                                            },   
                    highlight_function=lambda x: {'weight':2,'fillOpacity':0.9,'weight':0.5},    
                    tooltip=folium.features.GeoJsonTooltip(
                                            fields=tip_fields,
                                            aliases=tip_aliases)      
    ).add_to(m)


    # Save the map to an html file
    m.save(save_html)

    print(f"Made Map for {timepoint}, {var2map}")

#######################################################################################
## Set color schemes for the different maps
#######################################################################################
purple_scale =    ['#fcfbfd','#bcbddc','#9e9ac8','#807dba','#6a51a3','#54278f','#3f007d','#3f0267','#160124','#10011b']
green_red_scale = ['#006837','#1a9850','#66bd63','#a6d96a','#d9ef8b','#fee08b','#fdae61','#f46d43','#d73027','#a50026']
blue_red_scale =  ['#2a1d54','#1d2747','#347478','#4d8c78','#48855d','#41873e','#5bbd48','#b9c738','#c79a38','#8f320a']

scale2use = purple_scale

case_colors = [-10,1,10,25,50,75,100,250,500,1000,1500]
death_colors = [-10,1,3,5,7,10,15,20,35,50,75,100,150,200,250]
cp100k_colors = [-10,1,2,3,5,7,15,25,40,50,100]
dp100k_colors = [-10,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
pvax_colors = [-10,5,10,20,30,40,50,60,70,80,90]
temp_colors = [20,30,40,50,55,60,65,70,75,80,85]
#jcr_colors = [0,1,3,5,7,10,13,16,20,25,40]
jcr_colors = [0,3,6,10,15,20,20,25,30,40,45]

color_list = [0,0,0,0,0,0,0,0,0,0]

#######################################################################################
## Create maps for each month
#######################################################################################
for yyyy in range(1978,2020):
    print(f'{yyyy}0101')
    make_map(f'{yyyy}0101','job_creation_rate','job_creation_rate')

