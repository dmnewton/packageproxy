import re
pattern = re.compile('/data/')
data = '/data/'
print(re.search(pattern,data) )