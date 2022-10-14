FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

ENV http_proxy=http://MGC12F826PMD6T:8899

RUN apt-get update
RUN apt-get install -y curl  sudo git \
      openssh-server openssh-client python3.8 python3-distutils python3.8-dev 