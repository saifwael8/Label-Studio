# Label-Studio
This repository contains any label studio scripts that I use to automate my annotations tasks

**Converting from YOLOv8 (segmentation polygon) format to Label-Studio JSON format**
  1) Add your images folder path in the resize_images.py script
  2) A new folder named resized images containing 640x640 (resized images) will appear in the same directory you ran the script in
  3) Open the new_convert_yoloseg.py script and add the path of the input directory **path** at the end of the script
  4) The input directory should include **labels folder**, **classes.txt** and **images folder**
  5) Run the script
  6) The script will output **annotations.json** in the same directory it was ran in
  7) Import **annotations.json** to label studio and configure the labelling setup based on **classes.txt**
  8) To view the images correctly on LS, connect a local cloud storage ---> follow first 3 steps here: **https://labelstud.io/blog/tutorial-importing-local-yolo-pre-annotated-images-to-label-studio/**
  9) Finally you should be set

**Note:** You can change data in the script such as user name and other personalized data based on your own data, but they will not affect anything in importing the annotations. They'll just look cool :).
