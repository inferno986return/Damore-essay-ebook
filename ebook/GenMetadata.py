#GenMetadata.py - Generates the content.opf and toc.ncx files from the metadata.json file.

#opf = "OEBPS/content.opf"
#ncx = "OEBPS/toc.ncx"

#JSON extraction magic

import os
import json
from collections import OrderedDict

with open("metadata.json") as json_file:
    data = json.load((json_file), object_pairs_hook=OrderedDict) #For some reason the order is randomised, this preserves the order.

#Create a compatible content.opf from scratch.
def GenOPF():

    opf = open("content.opf", "w")
    opf.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?><package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">\n')

    #Metadata tags
    opf.write('\t<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n')
    opf.write('\t\t<dc:title>' + data["title"] + '</dc:title>\n')
    opf.write('\t\t<dc:creator>' + data["creator"] + '</dc:creator>\n')
    opf.write('\t\t<dc:subject>' + data["subject"] + '</dc:subject>\n')
    opf.write('\t\t<dc:publisher>' + data["publisher"] + '</dc:publisher>\n')
    opf.write('\t\t<dc:identifier id="bookid">' + data["ISBN"] + '</dc:identifier>\n')
    opf.write('\t\t<dc:language>' + data["language"] + '</dc:language>\n')
    opf.write('\t\t<dc:rights>' + data["rights"] + '</dc:rights>\n')
    opf.write('\t\t<meta content="main_cover_image" name="cover"/>\n')

    #Fixed (non-reflowable) support
    if data["textPresentation"] == "Reflowable" or "reflowable":
        print('e-book type: Reflowable')
        
    elif data["textPresentation"] == "Fixed layout" or "Fixed Layout" or "fixed layout" or "fixed":
        opf.write('\t\t<meta name="fixed-layout" content="true"/>\n')
        print('e-book type: Fixed layout')
    
    opf.write('\t</metadata>\n')

    #Manifest tags
    opf.write('\t<manifest>\n')

    #Write out the CSS files
    cssindex = 0

    for subdir, dirs, files in os.walk(data["containerFolder"] + os.sep + data["cssFolder"]):
        for file in files:
            filepath = subdir + os.sep + file
            correctfilepath = filepath.replace(data["containerFolder"] + os.sep, "") #removes the redudant OEBPS

            if filepath.endswith(".css"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="css' + str(cssindex) + '" media-type="text/css"/>\n')
                print (filepath)
                cssindex += 1           

    #Write out the NCX and cover image files
    opf.write('\t\t<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n')
    opf.write('\t\t<item href="'+ data["imagesFolder"] + '/' + data["epubCover"] +'" id="main_cover_image" media-type="image/jpeg"/>\n')

    #Write out the images

    imageindex = 0

    for subdir, dirs, files in os.walk(data["containerFolder"] + os.sep + data["imagesFolder"]):
        for file in files:
            filepath = subdir + os.sep + file
            correctfilepath = filepath.replace(data["containerFolder"] + os.sep, "") #removes the redudant OEBPS

            if filepath.endswith(".jpg") or filepath.endswith(".jpeg") or filepath.endswith(".png") or filepath.endswith(".gif") or filepath.endswith(".svg"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="image' + str(imageindex) + '" media-type="image/jpeg"/>\n')
                print (filepath)
                imageindex += 1

    #Write out all the pages in the book.
    #Count all the instances within the pages block.

    currentpage = 0
    totalpages = len(data["pages"]) #Number of pages

    while currentpage != totalpages: #Write out all the xhtml files as declared in the JSON.
        opf.write('\t\t<item href="' + data["pages"][currentpage]["fileName"] + '" id="' + str.lower(data["pages"][currentpage]["pageName"]) + '" media-type="application/xhtml+xml"/>\n')
        currentpage += 1
        
    #Write out all the custom fonts in the book.

    fontindex = 0

    for subdir, dirs, files in os.walk(data["containerFolder"] + os.sep + data["fontsFolder"]):
        for file in files:
            filepath = subdir + os.sep + file
            correctfilepath = filepath.replace(data["containerFolder"] + os.sep, "") #removes the redudant OEBPS

            if filepath.endswith(".ttf") or filepath.endswith(".otf") or filepath.endswith(".woff"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="font' + str(fontindex) + '" media-type="application/vnd.ms-opentype"/>\n')
                print (filepath)
                imageindex += 1

    opf.write('\t</manifest>\n')

    #Spine tags
    opf.write('\t<spine toc="ncx">\n')
    opf.write('\t\t<itemref idref="cover"/>\n')

    #Write out all the pagenumbers in order as declared in the JSON.
    currentpage = 0
    
    while currentpage != totalpages:
        opf.write('\t\t<itemref idref="'+ data["pages"][currentpage]["pageNumber"] +'"/>\n')
        currentpage += 1

    opf.write('\t</spine>\n')

    #End of file
    opf.write('</package>')

    opf.close() #Eventually save directly to the OEBPS folder

#Create a compatible toc.ncx from scratch.
def GenNCX():
   
    ncx = open("toc.ncx", "w")
    
    ncx.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    ncx.write('<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd"><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n')

    #Head tags
    ncx.write('<head>\n')
    ncx.write('\t<meta name="dtb:uid" content="-" />\n')
    ncx.write('\t<meta name="dtb:depth" content="1" />\n')
    ncx.write('\t<meta name="dtb:totalPageCount" content="0" />\n')
    ncx.write('\t<meta name="dtb:maxPageNumber" content="0" />\n')
    ncx.write('</head>\n')

    #Doctitle tags
    ncx.write('<docTitle>\n')
    ncx.write('\t<text>' + data["titleShort"] + '</text>\n')
    ncx.write('</docTitle>\n')

    #Write out the NavMap tags (and their children)
    ncx.write('<navMap>\n')

    currentpage = 0
    index = 1
    totalpages = len(data["pages"]) #Number of pages

    while currentpage != totalpages: #Write out all the xhtml files as declared in the JSON.
        #opf.write('\t\t<item href="' + data["pages"][currentpage]["fileName"] + '" id="' + str.lower(data["pages"][currentpage]["pageName"]) + '" media-type="application/xhtml+xml"/>\n')
        
        ncx.write('\t<navPoint id="navpoint-' + str(currentpage) + '" class="h' + str(index) + '" playOrder="' + str(index) + '">\n') #id=001 class=h1 playOrder=1
        ncx.write('\t\t<navLabel>\n')
        ncx.write('\t\t\t<text>' + data["pages"][currentpage]["pageName"] + '</text>\n')
        ncx.write('\t\t</navLabel>\n')
        ncx.write('\t\t<content src="'+ data["pages"][currentpage]["fileName"] +'" />\n') #title.xhtml
        ncx.write('\t</navPoint>\n')

        currentpage += 1
        index += 1
    
    ncx.write('</navMap>\n')
    
    #End of file
    ncx.write('</ncx>')

GenNCX()
GenOPF()
