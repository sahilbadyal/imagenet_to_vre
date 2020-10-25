#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2
from random import sample
import os
import json


# In[2]:


with open('syntoword.json', 'r') as f:
    syntoword = json.load(f)
with open('attribMap.json', 'r') as f:
    attribMap = json.load(f)


# In[3]:


np.random.seed(42) ## Done for reproducibility


# In[22]:


def create_collage(input_dir, collage_size):
    '''
    This function creates the 3 X 3 collage of randomly sampled images from the input directory
    '''
    r, c = collage_size
    images_outers= []
    image_names = []
    for i in range(r):
        images = []
        for image_name in sample(os.listdir(input_dir), c):
            image_names.append(image_name)
            image = cv2.imread(os.path.join(input_dir, image_name))
            try:
                image = cv2.resize(image, (300, 200)) #If something fails here
            except:
                print(image_name)
            images.append(image)
        image_outer = np.hstack(images)
        images_outers.append(image_outer)
    return ((np.vstack(images_outers)), image_names)


# In[5]:


#hardcoded location references only if the attributres are not present 
location_ref = {
    0: "on the top left",
    1: "on the top",
    2: "on the top right",
    3: "to the left",
    4: "in the middle",
    5: "to the right",
    6: "on the bottom left",
    7: "on the bottom",
    8: "on thebottom right"
}


# In[6]:


bounding_boxes = {
    0: [0,0, 300, 200],
    1: [300,0, 300, 200],
    2: [600,0, 300, 200],
    3: [0,200, 300, 200],
    4: [300, 200, 300, 200],
    5: [600, 200, 300, 200],
    6: [0, 400, 300, 200],
    7: [300, 400, 300, 200],
    8: [600, 400, 300, 200]
}


# In[7]:


def markFaultyFiles(input_dir):
    '''
    This function marks the faulty/damaged/corrupt images that are present in the input dir
    '''
    image_names = []
    for image_name in os.listdir(input_dir):
        image = cv2.imread(os.path.join(input_dir, image_name))
        try:
            image = cv2.resize(image, (300, 200))
        except:
            #print(image_name)
            image_names.append(image_name)
    return image_names


# In[8]:


def deleteFiles(inp_dir, files):
    '''
    Deletes the files in a directory
    '''
    for file in files:
        os.remove(os.path.join(inp_dir,file))


# In[9]:


def createRefStatement(id_, syn, synid):
    '''
    Basic function that creates a reference statement from the image arrtibues and its synset name
    http://image-net.org/download-attributes
    '''
    global location_ref
    objectNames = syntoword[syn]
    if len(objectNames) == 0:
        return ""
    i  = np.random.randint(0,len(objectNames))
    ref = "the"
    attrib = " "
    if len(attribMap[synid]['attrib']) != 0:
        if len(attribMap[synid]['attrib']) == 1:
            attrib += attribMap[synid]['attrib'][0]
        else:
            attrib += ", ".join(attribMap[synid]['attrib'][:-1])
            if(len(attribMap[synid]['attrib']) >2):
                attrib += ", "
            else:
                attrib += " "
            attrib += "and " + attribMap[synid]['attrib'][-1]
        ref += attrib + " " + objectNames[i]
    else:
        try:
            ref +=  " " + objectNames[i] + " " + location_ref[id_]
        except:
            #print(objectNames,i,syn, synid)
            pass
    return ref


# In[10]:


def checkAndCreateDirectory(direc, create=True):
    '''
    This function checks if a directory exits and creates it if the flag is true
    '''
    if os.path.isdir(direc):
        return True
    if create:
        os.mkdir(direc)
    return False


# In[20]:


def createDataset(inp_dir, out_dir, length=130):
    '''
    The main loop that created the dataset and stores the information in the output directory
    
    '''
    total_files = 0
    inputcheck = checkAndCreateDirectory(inp_dir, False)
    if not inputcheck:
        raise ValueError(f"Input directory {inp_dir} does not exist. Exiting...")
    checkAndCreateDirectory(out_dir)
    
    global bounding_boxes
    
    reference_image = "ref_image_"
    output_dataset = {}

    output_dataset['boxes'] = []
    output_dataset['images'] = []

    for key in bounding_boxes:
        bb = {}
        bb['box_id'] = key
        bb['name'] = ''
        bb['width'] = bounding_boxes[key][2]
        bb['height'] = bounding_boxes[key][3]
        bb['x'] = bounding_boxes[key][0]
        bb['y'] = bounding_boxes[key][1]
        output_dataset['boxes'].append(bb)

    for i in range(length):
        #print(i)
        image, images = create_collage(inp_dir, (3,3))
        datum = {}
        image_name  = reference_image + str(i)
        datum['filename'] = image_name
        datum['reference_pairs']  = []
        previous_ref = [] ## there should not be same reference in the same collage
        for j,img in enumerate(images):
            synid = img.split('.')[0]
            syn  = synid.split('_')[0]
            bb = {
                'boundingBox_id':j
            }
            ref = createRefStatement(j, syn, synid)
            if ref == "":
                print(img)
                continue
            if ref not in previous_ref:
                total_files += 1
                bb['reference'] = ref
            else:
                continue
            previous_ref.append(ref)
            datum['reference_pairs'].append(bb)
        output_dataset['images'].append(datum)
        cv2.imwrite(f"{os.path.join(out_dir,image_name)}.jpg", image)
    print(f"Total Datapoints Generated  = {total_files}")
    return output_dataset


# In[12]:


def saveDataset(out_dir,output_dataset):
    with open(out_dir+"vre_dataset.json", 'w') as f:
        json.dump(output_dataset,f)


# In[24]:


input_directory  = "./data/"
output_directory = "./dataset_v3/"

# Delete the faulty files, sanity check
#deleteFiles(input_directory,markFaultyFiles(input_directory))

## create the dataset

ds = createDataset(input_directory,output_directory,length=320)

## Save the dataset
saveDataset(output_directory, ds)


# In[ ]:





# In[ ]:




