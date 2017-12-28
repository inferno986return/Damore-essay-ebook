#!/usr/bin/env python

#GenEpub.py - Generates an .epub file from the data provided. Ideally with no errors or warnings from epubcheck.

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
zf.close()




