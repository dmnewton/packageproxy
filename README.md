# packageproxy

## issue with source IP on Mac
<br> you always get the ip address of the bridge!

https://github.com/docker/for-mac/issues/180

https://stackoverflow.com/questions/67128839/how-can-i-get-the-users-ip-address-in-my-cloud-run-flask-app


## start server

```
drun.sh

cd proxypi

python3 proxypi

```

## start client

```
docker run -it --rm python:slim bash

apt intall vim

vi /etc/apt/apt.conf.d/proxy.conf

Acquire::http::Proxy "http://MGC12F826PMD6T:8899/";
```


```


apt update

apt install iputils-ping

```