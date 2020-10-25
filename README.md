# ImageNet to VRE

### Basic Introduction

This repository contains the code for converting the imagenet attributes dataset to a Visual Referring Expression (VRE) dataset. 

**Original Dataset**

[Imagenet Attributes](http://image-net.org/download-attributes)

The imagenet attribute dataset is a new addition to the already famous dataset. They used Amazon mechanical turk to tag the following atrtributes in the images

* Color: *black, blue, brown, gray, green, orange, pink, red, violet, white, yellow*
* Pattern: *spotted, striped*
* Shape: *long, round, rectangular, square*
* Texture: *furry, smooth, rough, shiny, metallic, vegetation, wooden, wet*

I have used a simple yet effective algorithm to convert this into a VRE dataset:

**Algorithm**
1. Create a 3x3 collage of images from the original dataset by scaling each image to a fixed size (say 300 by 200 pixels).
2. For each sub-image:
    1. Save its bounding box (or boundaries in the collage).
    2. Create the referring expression with the following rule
    
    
        > the \<comma separated attributes\> \<synset name\>
        
Examples are shown below.

This creates 9 referring expressions per collage. 


### How to use/view and Replicate this work?

#### Use the dataset (Dropbox account is required (create one if does not exist, its free!))

1. Download dataset from [here](https://www.dropbox.com/s/fjwtkxmr7r3457z/dataset_v3.zip?dl=0).

#### View

1. Clone this repository

2.  Download dataset from [here](https://www.dropbox.com/s/fjwtkxmr7r3457z/dataset_v3.zip?dl=0).

3. Run `dataset_browser.py` to view the images and bounding boxes.

### Replicate

1. Clone this repository

2. Download the original dataset from [here](https://www.dropbox.com/s/lie7skiozji619g/data.zip?dl=0). [optional]

3. Unzip the original dataset in the top level project directory.

```
unzip data.zip
```

4. Run the `create_dataset.py` (make sure to check input directory is pointed to ./data)

5. This will create the output folder with *vre_dataset.json*


### Directory structure and files

├── README.md ->   *you are here*<br/>
├── __init__.py ->        *tell python its a module*<br/>
├── create_dataset.py -> *used to create the dataset*<br/>
├── dataset_browser.py -> *used to view the dataset*<br/>
├── imagenet_attributes -> *this folder contains the original imagement attributes dataset*<br/>
│   └── attrann.mat -> *original dataset mat file*<br/>
├── json -> *contains all the jsons required to create this dataset*<br/>
│   ├── attribMap.json -> *maps an image to its attributes*<br/>
│   ├── syntoid.json -> *maps a synset to the images contained*<br/>
│   └── syntoword.json -> *maps a synset to the associated words*<br/>
├── notebooks -> *Jupyter Notebooks*<br/>
│   ├── Dataset Browser.ipynb -> *parent notebooks of the dataset browser <now deprecated>*<br/>
│   ├── DatasetCreation.ipynb -> *parent notebooks of the create dataset <now deprecated>*<br/>
│   ├── DownloadImages.ipynb -> *useful for downloading the images using attran.mat*<br/>
│   ├── GetSynnetWords.ipynb -> *creates the synttoword.json*<br/>
│   ├── ImageAttrib.ipynb -> *creates the attribMap.json*<br/>
│   └── SynToID.ipynb -> *creates the stntoid.json*<br/>
└── vre_globals.py -> *stores the global dictionaries*<br/>
