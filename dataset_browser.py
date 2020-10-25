#!/usr/bin/env python
'''
Author: Sahil Badyal
This module contains the functions to view the  imagenet VRE dataset
'''
import json
import cv2
import numpy as np
import os
import sys
from vre_globals import bounding_boxes

def showImage(x):
    '''
    Shows the image and waits for the user input infinitely
    '''
    cv2.imshow("image", x)
    if cv2.waitKey(0)==ord('e'):
        sys.exit()
    #closing all open windows
    cv2.destroyAllWindows()

def createBoundingBox(img , bb):
    '''
    Creates a green bounding box
    '''
    cv2.rectangle(img, (bb[0], bb[1]), (bb[0]+bb[2], bb[1]+bb[3]), (0, 255, 0), 2)


inp_dir = './dataset_v3/'
path  = os.path.join(inp_dir, 'vre_dataset.json')
with open(path, 'r') as f:
    dataset = json.load(f)

for i,datum in enumerate(dataset['images']):
        for reference_pair in datum['reference_pairs']:
            x = cv2.imread(os.path.join(inp_dir+datum['filename']+'.jpg'))
            createBoundingBox(x, bounding_boxes[reference_pair['boundingBox_id']])
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(x, reference_pair['reference'], (10,400), font, 1, (0, 0, 255), 3)
            showImage(x)
