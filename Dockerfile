FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y git curl \
      python3.9 python3-distutils python3.9-dev bind9-dnsutils 

# WE ARE NOT GOING TO USE THE UBUNTU SYSTEM PACKAGE MANAGER FOR PYTHON PACKAGES.  SO WE WILL USE PIP.

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

RUN python3 get-pip.py

RUN pip3 install httpserver

ARG USER=dnewton
ARG USER_ID=1000
ARG GROUP_ID=1001

RUN groupadd -g $GROUP_ID -o $USER


# adding --no-log-init for large UID 
RUN useradd -m -u $USER_ID -g $GROUP_ID -s /bin/bash $USER
RUN chown -R ${USER} /home/${USER}

# Setup default user, when enter docker container
USER ${USER_ID}
WORKDIR /home/${USER}

EXPOSE 8899