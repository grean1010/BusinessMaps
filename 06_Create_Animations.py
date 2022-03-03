#######################################################################################
## Title:   06_Create_Animations.py
## Author:  Maria Cupples Hudson
## Purpose: Put screenshots together into a video. Add music.
## Updates: 10/14/2019 Code Written
##          06/03/2020 Updated to work with Coronavirus data
##          03/03/2022 Updated to be use BSD data
#######################################################################################
##
##
#######################################################################################
import imageio
import glob
import os
from moviepy.editor import *
from PIL import Image 

# location of this folder on the hard drive
base_loc = os.path.join('C:\\','Users','laslo','OneDrive','Documents','Maria','BusinessMaps')

# Set locations 
png_path = os.path.join(base_loc,'map_png')
temp_file = os.path.join(png_path,'temp.png')
animation_path = os.path.join(base_loc,'animations')

#######################################################################################
## Create a function to open web browser, load page, take a screenshot and save it
#######################################################################################
def animate_map(name2find,fileout,fpsvalue,musicfile):

    # Go through the images and find the smallest height and width
    fileList = []
    min_h = 10000
    min_w = 10000

    
    # Go through the list of png files for this animation
    for file in os.listdir(png_path):
    
        #print(f'Checking file {file}')
    
        if file.startswith(name2find):
            
            #print(f'Found file {file}')
        
            # Find the complete path name of each image and add to the list
            complete_path = os.path.join(png_path,file)        
            fileList.append(complete_path)
        
            # check to see if this is the lowers height/width so far. Update if it is.
            img = Image.open(complete_path) 
            width, height = img.size
        
            if width < min_w:
                min_w = width
    
            if height < min_h:
                min_h = height

    # Create a writer for the animation file/mp4
    writer = imageio.get_writer(os.path.join(animation_path,f'{fileout}.mp4'), fps=fpsvalue)

    # Go through the list of png files to add to the animation
    for im in fileList:

        # to resize and set the new width and height 
        img = Image.open(im)

        # find the current image size
        width, height = img.size

        # resize withe same center so that all files are at the same/minimum size
        top = int((height - min_h)/2)
        bottom = int(height - (height - min_h)/2)
        left = int((width - min_w)/2)
        right = int(width - (width - min_w)/2)
 
        # perform the crop and save to a temporary file
        cropped = img.crop((left,top,right,bottom))
        cropped.save(temp_file)
    
        # add the temporary file to the animation
        writer.append_data(imageio.imread(temp_file))

        print(f"Added {im}")
    
    # finalize and close the animation
    writer.close()
    
    # Add music
    music = os.path.join(base_loc,f'{musicfile}')
    original = os.path.join(animation_path,f'{fileout}.mp4')
    final_out = os.path.join(animation_path,f'{fileout}_WithSound.mp4')
    
    # Pull the video portion and determine the length of the clip. Add 5 Secconds.
    video1 = VideoFileClip(original)
    duration = video1.duration + 5

    # Pull the audio, 5 seconds longer than the clip
    audio = AudioFileClip(music).subclip(0, duration)
    video1 = VideoFileClip(original)
    final = video1.set_audio(audio)
    final.write_videofile(final_out,codec= 'mpeg4')
    
    
    print('Done!!!')

animate_map('job_creation_rate','Job_Creation_Rate',2,'Flying_Free.mp3')