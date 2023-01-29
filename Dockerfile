FROM python:slim

ARG DEBIAN_FRONTEND=noninteractive

COPY requirements.txt .

RUN pip3 install -r requirements.txt

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