#!/bin/sh
ffmpeg -f v4l2 -s 1440x1440 -r 15 -i /dev/video1 -map 0:v -vcodec rawvideo -vf format=yuv420p -f v4l2 /dev/video2
