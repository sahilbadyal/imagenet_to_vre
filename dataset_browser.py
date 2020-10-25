#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import cv2
import numpy as np


# In[2]:


with open('dataset_v1/vre_dataset.json', 'r') as f:
    dataset = json.load(f)


# In[3]:


def showImage(x):
    cv2.imshow("image", x)
    cv2.waitKey(0)
    #closing all open windows
    cv2.destroyAllWindows()
    #cv2.waitKey(0)


# In[4]:


def createBoundingBox(img , bb):
    cv2.rectangle(img, (bb[0], bb[1]), (bb[0]+bb[2], bb[1]+bb[3]), (0, 255, 0), 2)


# In[5]:


for i,datum in enumerate(dataset):
        if 'ref' not in datum:
            continue
        x = cv2.imread('./dataset_v1/images/'+datum['image']+'.jpg')
        createBoundingBox(x, datum['bb'])
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(x, datum['ref'], (10,400), font, 1, (0, 255, 0), 2)
        showImage(x)


# In[ ]:




