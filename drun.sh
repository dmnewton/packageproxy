#docker run -c 2 --memory=2g -it -p 8899:8899 proxypy:latest proxy --hostname 0.0.0.0
#docker network rm tulip-net
#docker network create -d overlay tulip-net
docker run -c 2 --memory=2g -it --rm --name proxyserver --user=dnewton -p 8899:8899 -v /Users/dnewton/dockerimages/proxypi/proxypy:/home/dnewton/proxypy  proxypy:latest bash