# HoloObjectDetectionTraining

## YOLO v2 (aka YOLO 9000)
YOLO9000 is a high speed, real time detection algorithm that can detect on OVER 9000! (object categories)

link : https://pjreddie.com/darknet/yolo/

## Requirements
Python 3.6. Anaconda

Tensorflow CPU

openCV (https://www.lfd.uci.edu/~gohlke/pythonlibs/)

Took files from Darkflow repo 
https://github.com/thtrieu/darkflow

extract the files in the root folder

## Step 1 - Build the library
python setup.py build_ext --inplace

## Step 2 - Download a weights file
Download the YOLOv2 608x608 weights file here (https://pjreddie.com/darknet/yolo/)

NOTE: there are other weights files you can try if you like

create a bin folder within the darkflow-master folder

put the weights file in the bin folder
