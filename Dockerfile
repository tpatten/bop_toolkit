FROM ubuntu:18.04

ENV TZ=Europe/Vienna
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y wget bash zip rsync python3-venv python3-dev build-essential software-properties-common

RUN apt-get install -y python3-pip libgl1-mesa-glx libglfw3 freetype2-demos python3-opencv xvfb

RUN python3.6 -m pip install numpy==1.14.5 \
                             scipy==1.5.1 \
                             imageio==2.5.0 \
                             pypng==0.0.19 \
                             pytz \
                             Cython==0.29.10 \
                             PyOpenGL==3.1.0

RUN python3.6 -m pip install glumpy==1.1.0
