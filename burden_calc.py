# PIL and csv are not standard libraries
# It's best to create a virtual environment and install them with
# pip install python-csv
# pip install Pillow

import os
import csv
from PIL import Image
import numpy as np
from tqdm import tqdm

path='data/' #path to your data
files_all=os.listdir(path)
# filter down to filenames that end with '.tif'
files=[file for file in files_all if file.endswith('.tif')]

# files is a list of all the files that end in .tif, to remove anything else, including hidden files
#for file in files_all:
#    if '.tif' in file:
#        files.append(file)

# The list of channels. This can be changed to user input later
channels=['AT180',
          'CD68',
          'CD68AT180',
          'CD68GAD',
          'CD68GADAT180',
          'CD68GFAP',
          'GAD',
          'GADAT180',
          'GFAP',
          'GFAPAT180',
          'GFAPGAD',
          'GFAPGADAT180']

print('The following channels will be used as default')
for channel in channels: print(channel)

def user_channels():
    channels=[]
    print("Enter channel names. type 'done' to finish")
    while True:
        usr_input=input(":")
        if usr_input.lower()=="done":
            return(channels)
        else:
            channels.append(usr_input)

while True:
    new_chan=input("Would you like to set new channels? (y/n) ")
    if new_chan.lower() == "n":
        break
    elif new_chan.lower() == "y":
        chan_temp=user_channels()
        if len(chan_temp) == 0:
            print("!!!WARNING!!! You didn't enter any channel names")
            print("!!!WARNING!!! Keeping standard channel names")
        else:
            channels=chan_temp
            del(chan_temp)
        break
    else:
        continue

# Create a matching string and test if the channels are all present in the data
for channel in channels:
    text_to_match='-'+channel+'.tif'

    if any(text_to_match in file for file in files):
        print(f"Channel {channel} found")
    else:
        print(f"!!!WARNING!!! Channel {channel} was NOT found")

# Simple check that the number of channels and files are consistent
if len(files) % len(channels) != 0:
    print("!!!WARNING!!! The number of files is not a multiple of the number of channels")

# Identify the names of the image stacks
# This assumes that the channel name comes immediately before the first instance of '.tif' in the file name
# and after the last hyphen in the filename. The stack name is assumed to be everythtning before that hyphen
# Using a set, rather than a list, automatically deduplicates
stacks=set()
for file in files:
    fname_noext=file[0:file.find('.tif')]
    stacks.add(fname_noext[0:fname_noext.rindex('-')])

# Turn it back into a list and sort the stack names alphabetically
stacks=list(stacks)
stacks.sort()
print("The following stacks were found:")
for stack in stacks: print(stack)

while True:
    exitchoice = input("Would you like to proceed? (y/n) ")
    if exitchoice.lower() == "y":
        break
    elif exitchoice.lower() == "n":
        quit()
    else:
        continue

print('Starting the analysis')


# Create 2d array. Stacks are rows, channels are columns
burden=np.zeros([len(stacks),len(channels)])

for i,file in enumerate(tqdm(files)): # loop over all the files
    skip = True
    # identify which stack we're looking at from the filename
    for j,stack in enumerate(stacks):
        if stack in file:
            sec_i=j
    # identify which channel we're looking at from the filename
    # If there are files for channels that the user hasn't inputed
    # those files will be skipped
    for j, channel in enumerate(channels):
        if '-'+channel+'.tif' in file:
            chn_i=j
            skip=False
    if skip: continue

    # open the image file and count the number of non-zero voxels in each image
    with Image.open(path+file) as himg:
        page=int()
        imsize=int()
        nbright=int()
        while True: # Looping over each image in the stack
            try:
                himg.seek(page)
                img=np.asarray(himg)
                if page==0:
                    imsize=img.shape
                nbright+=np.count_nonzero(img>0)
                page+=1
            except EOFError:
                break

    # Total number of voxels
    tot_vxl=int(page*imsize[0]*imsize[1])

    # Calculate the burden as a percentage, put it in the correct cell in the 2-d array
    burden[sec_i,chn_i]=100*nbright/tot_vxl


# Write the results out to a csv file
with open("results.csv",'w') as outfile:
    writer=csv.writer(outfile)
    writer.writerow(['stack']+channels)
    for i, stack in enumerate(stacks):
        writer.writerow([stack]+list(burden[i,:]))