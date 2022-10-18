import socket
import os
import yaml 

try:
  s=socket.getaddrinfo('www.google.com', 80)
  print('no proxy set')
except:
  with open('proxypy/security_rules.yaml') as file:
        config_data_input = yaml.load(file, Loader=yaml.FullLoader)
  proxy = config_data_input.get('proxy')
  os.environ["http_proxy"] = proxy.get('http_proxy')
  os.environ["https_proxy"] = proxy.get('https_proxy')
  os.environ["no_proxy"] = proxy.get('no_proxy')
  print('proxy set')