#!/usr/bin/env python

from time import time
from xmlrpc.client import Boolean

from attr import dataclass
import set_proxy

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import argparse
import logging
import sys
import yaml
import re

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

chunksize = 1024

last_update = time() 

@dataclass
class ConfigData:
    server: set
    clients: set
    packages: list

def check_requester(addr: str) -> Boolean:
    nn = socket.getnameinfo((addr, 0), 0)
    logger.info("client name %s", nn[0])
    global config_data
    if nn[0] in config_data.clients:
        return False
    else:
        logger.info("unknown client name %s", nn[0])
        return  True

def check_server(addr: str)  -> Boolean:
    logger.info("server name %s", addr)
    global config_data
    if addr in config_data.server:
        return False
    else:
        return  True

def check_url(path: str)  -> Boolean:
    logger.info("path %s", path)
    for x in config_data.packages:
        if re.search(x,path):
            return False 
    return True

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET(body=False)

    def do_GET(self, body=True):

        if check_requester(self.client_address[0]):
            self.send_error(403, u'security client not allowed')
            return

        url = self.path
        o = urlparse(url)

        if check_server(o.hostname):
            self.send_error(403, u'security repository not allowed')
            return


        if check_url(o.path):
            self.send_error(403, u'security url')
            return


        
        req = Request(url=url)
        resp = urlopen(req)
        self.send_response(resp.getcode())
        respheaders = resp.info()
        for key, value in respheaders._headers:
            self.send_header(key, value)
        self.end_headers()
        if body:
            chunk = resp.read(chunksize)
            while chunk:
                self.wfile.write(chunk)
                chunk = resp.read(chunksize)

    def log_request(self, code: int | str = ..., size: int | str = ...) -> None:
        return
        # return super().log_request(code, size)


def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Simple Proxy')
    parser.add_argument('--port', dest='port', type=int, default=8899,
                        help='serve HTTP requests on specified port (default: 8899)')
    args = parser.parse_args(argv)
    return args

def on_modified(event):
    global last_update  
    new_update = time()
    diff = new_update - last_update
    if diff > 1 :
        last_update = new_update
        logger.info(f"file modified  {event.src_path}")
        load_security()

def load_security():
    with open('proxypy/security_rules.yaml') as file:
        config_data_input = yaml.load(file, Loader=yaml.FullLoader)

    global config_data

    config_data = ConfigData(
        server=set(config_data_input.get('server')),
        clients=set(config_data_input.get('clients')),
        packages=[ re.compile(x) for x in config_data_input.get('packages')]
    )

def main(argv=sys.argv[1:]):
    args = parse_args(argv)
    logger.info('http server is starting on port {}...'.format(args.port))
    server_address = ('0.0.0.0', args.port)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    logger.info('http proxy is running ')


    patterns = ["*.yaml"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_modified = on_modified

    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()

    load_security()
 
    httpd.serve_forever()


if __name__ == '__main__':
    main()