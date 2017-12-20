#GenMetadata.py - Generates the content.opf and toc.ncx files from the metadata.json file.

#opf = "EBOOK/content.opf"
#ncx = "EBOOK/toc.ncx"

#JSON extraction magic

import json
from collections import OrderedDict

with open("metadata.json") as json_file:
    data = json.load((json_file), object_pairs_hook=OrderedDict) #For some reason the order is randomised, this preserves the order.

#Create a compatible content.opf from scratch.
def GenOPF():

    opf = open("content.opf", "w")
    opf.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?><package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">\n')

    #Metadata tags
    opf.write(' <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n')
    opf.write('  <dc:title>' + data["title"] + '</dc:title>\n')
    opf.write('  <dc:creator>' + data["creator"] + '</dc:creator>\n')
    opf.write('  <dc:subject>' + data["subject"] + '</dc:subject>\n')
    opf.write('  <dc:publisher>' + data["publisher"] + '</dc:publisher>\n')
    opf.write('  <dc:identifier id="bookid">' + data["ISBN"] + '</dc:identifier>\n')
    opf.write('  <dc:language>' + data["language"] + '</dc:language>\n')
    opf.write('  <dc:rights>' + data["rights"] + '</dc:rights>\n')
    opf.write('  <meta content="main_cover_image" name="cover"/>\n')
    opf.write(' </metadata>\n')

    #Manifest tags
    opf.write(' <manifest>\n')
    opf.write('  <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n')
    opf.write('  <item href="images/' + data["epubCover"] +'" id="main_cover_image" media-type="image/jpeg"/>\n')
    
    #Write out all the pages in the book.
    #Count all the instances within the pages block.

    #currentpage = 0
    #totalpages = #Number of pages
   
    #while (totalpages < currentpage):
        #opf.write('   <item href="" id="" media-type="application/xhtml+xml"/>\n')
        #currentpage = currentpage + 1
    
    opf.write(' </manifest>\n')

    #Spine tags
    opf.write(' <spine toc="ncx">\n')  
    opf.write('  <itemref idref="cover"/>\n')

    #Need to increment for each page.
    print (data["pages"])
    
    #currentpage = 0
    #while (totalpages < currentpage):
        #opf.write('  <itemref idref="'+ pagecount +'"/>\n')
        #currentpage = currentpage + 1
    

    opf.write(' </spine>\n')

    #End of file
    opf.write('</package>')

    opf.close()
    
GenOPF()
