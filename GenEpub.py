#!/usr/bin/env python

#GenEpub.py - Generates an .epub file from the data provided.
#Ideally with no errors or warnings from epubcheck (needs to be implemented, maybe with the Python wrapper).

import os
import json
import zipfile
    
with open('metadata.json') as json_file:
        data = json.load(json_file)

#The ePub standard requires deflated compression and a compression order.
zf = zipfile.ZipFile(data["fileName"] + '.epub', 'w', zipfile.ZIP_STORED)

zf.write(data["fileName"] + '/mimetype')

for dirname, subdirs, files in os.walk(data["fileName"] + '/META-INF'):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))

for dirname, subdirs, files in os.walk(data["fileName"] + '/EBOOK'):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))

#zipfile has a built-in validator for debugging
if zipfile.is_zipfile(zf) is True:
    print("ZIP file is valid.")

#Extra debugging information
#print(getinfo.compress_type(zf))
#print(getinfo.compress_size(zf))
#print(getinfo.file_size(zf))

zf.close(zf)

