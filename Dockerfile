FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y wget bash zip rsync python3-venv python3-dev build-essential software-properties-common

RUN apt-get install -y python3-pip libgl1-mesa-glx libglfw3 freetype2-demos python3-opencv xvfb

RUN python3.6 -m pip install numpy \
                             imageio==2.5.0 \
                             pypng==0.0.19 \
                             pytz \
                             scipy==1.5.1 \
                             Cython==0.29.10 \
                             glumpy==1.1.0 \
                             PyOpenGL==3.1.0 \
                             opencv-python
