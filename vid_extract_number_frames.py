'''
Extracts frames from an input video as images, 
adds frame-number to those images, and saves them as JPEGS.
Can also print video metadata.

Usage: python vid_extract_number_frames.py input_file output_directory


2023-May-16: First version (DM)
'''

import os
import sys
import cv2

# The two below are just for printing out video metadata
import ffmpeg
from pprint import pprint # for printing Python dictionaries

media_file = sys.argv[1]  # input video
op_dir = sys.argv[2]      # directory to store output frames


#####################################################################
def extract_number_save_frames (video_file, opdir):

    if not os.path.exists(opdir):
        os.makedirs(opdir)

    vidcap = cv2.VideoCapture(video_file)
    font = cv2.FONT_HERSHEY_SIMPLEX
    success,image = vidcap.read()
    count = 0

    while success:
        cv2.putText(image, str(count), (50, 50), font, 1,
                (0, 255, 255), 2, cv2.LINE_4)

        opfile = 'frame' + f'{count:05d}' + '.jpg'
        cv2.imwrite(os.path.join(opdir , opfile), image)

        success,image = vidcap.read()
        print('Read frame number: ', count, 'status:',success)
        count += 1

    return 0
#####################################################################


#####################################################################
def print_video_metadata (video_file):

    pprint(ffmpeg.probe(video_file)["streams"])
    return 0
#####################################################################

    
ret = print_video_metadata (media_file)

ret = extract_number_save_frames (media_file, op_dir)


