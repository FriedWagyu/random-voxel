#!/bin/bash

cd /home/pi/Desktop/random-voxel/

git pull

cd /home/pi/Desktop/random-voxel/op_mkv/

while [ 1 -gt 0 ]
do
FILE=$(ls | shuf -n 1)
echo $FILE
omxplayer $FILE
done