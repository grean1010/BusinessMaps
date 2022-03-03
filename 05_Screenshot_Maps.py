#######################################################################################
## Title:   05_Screnshot_Maps.py
## Author:  Maria Cupples Hudson
## Purpose: Open HTML files and take a screenshot
## Updates: 10/14/2019 Code Written
##          06/03/2020 Updated to work with Coronavirus data
##          03/03/2022 Updated to work with BSD
#######################################################################################
##
##
#######################################################################################
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# location of this folder on the hard drive
base_loc = os.path.join('C:\\','Users','laslo','OneDrive','Documents','Maria','BusinessMaps')

# Set locations 
map_html = os.path.join(base_loc,'map_html')
map_png = os.path.join(base_loc,'map_png')


s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()

#######################################################################################
## Create a function to open web browser, load page, take a screenshot and save it
#######################################################################################
def take_pictures(timepoint,SaveName):

    save_html = os.path.join(map_html,f'{SaveName}_{timepoint}.html')
    save_png = os.path.join(map_png,f'{SaveName}_{timepoint}.png')
    
    # Open a browser window...
    browser = webdriver.Chrome(service=s)

    #..that displays the map...
    browser.get(save_html)

    # maximize window
    browser.maximize_window()
    
    # Give the map tiles some time to load
    time.sleep(5)

    # Grab the screenshot and save it as a png file
    browser.save_screenshot(save_png)
    
    # Close the browser
    browser.quit()
    
#######################################################################################
## Create maps for each day
#######################################################################################
# Screenshot each map

for yyyy in range(1978,2020):
    print(f'{yyyy}0101')
    take_pictures(f'{yyyy}0101','job_creation_rate')