# BusinessMaps

I'm experimenting with the 2019 BDS-- available for download here:

https://www.census.gov/programs-surveys/bds/news-updates/updates/2019-bds-release.html

I pulled csv files and read them into Python.  Then I manipulated the data so I could get the job creation rate for each county and each year from 1978 to 2019.

I resued a great deal of code from my Cornavirus Map Animation project as well as my original Map Animation project from 2019.  This could use some clean-up in several areas:
1. I would like to understand the data better so I can make more meaningful maps.
2. I would like to clean up the county-level maps for years prior to 2000. 
3. I would like to play with the color levels in the maps to see if patterns could be better illuminated.

The project has 6 basic steps:
1. Create initial geojson files that have the shape of each county in the US during each year.
2. Reformat the data so that it is at the county level with one column per year for the job creation rate.
3. Add the job creation rate to each year-specific geojson file.
4. Create HTML maps for each year.
5. Take a screenshot of each year's HTML file.
6. Put the screenshots together into a video.

You can see the video that I created here:

https://youtu.be/4Ma0VcbSUks
