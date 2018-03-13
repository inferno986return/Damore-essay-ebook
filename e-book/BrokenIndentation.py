#BrokenIndentation.py - Fix the indentation levels of 2, 3 and 4.

import os
import time
import json
from collections import OrderedDict
import zipfile

with open("metadata.json") as json_file:
    data = json.load((json_file), object_pairs_hook=OrderedDict) #For some reason the order is randomised, this preserves the order.
    #Page indentation.

    currentpage = 7
    index = 1

    #Constants
    totalpages = len(data["pages"]) #Number of pages
    indentation = 1 #This is a constant as the ePub standard allows upto 4 levels.
    twoindentation = 2
    threeindentation = 3
    fourindentation = 4

if twoindentation == data["pages"][currentpage]["indentation"]:
    #for twoindentation in data["pages"][currentpage]["indentation"]:
        print('indent is 2')

        addNCXpages()
        addNCXanchors()

elif threeindentation == data["pages"][currentpage]["indentation"]:
    #for threeindentation in data["pages"][currentpage]["indentation"]:
        addNCXpages()
        addNCXanchors()

elif fourindentation == data["pages"][currentpage]["indentation"]:

else:
    print('No pages were printed.')

print('\t</navPoint>\n')

    #Write out the pages
    def addNCXpages()
        index += 1
        print('\t<navPoint id="navpoint-' + str(index) + '" playOrder="' + str(index) + '">\n') #id=001 class=h1 playOrder=1
        print('\t\t<navLabel>\n')
        print('\t\t\t<text>' + data["pages"][currentpage]["pageName"] + '</text>\n')
        print('\t\t</navLabel>\n')
        print('\t\t<content src="' + data["pages"][currentpage]["fileName"] + '" />\n')

    #Write out the page's anchor tags.
    def addNCXanchors()
        try:
            currentanchor = 0
            totalanchors = len(data["pages"][currentpage]["anchorNames"])

            while currentanchor != totalanchors:
                index += 1

                print('\t\t<navPoint id="navpoint-' + str(index) + '" playOrder="' + str(index) + '">\n') #id=001 class=h1 playOrder=1
                print('\t\t\t\t<navLabel>\n')
                print('\t\t\t\t\t<text>' + data["pages"][currentpage]["anchorNames"]["anchorName" + str(currentanchor) + ""] + '</text>\n')
                print('\t\t\t\t</navLabel>\n')
                print('\t\t\t\t<content src="'+ data["pages"][currentpage]["fileName"] + data["pages"][currentpage]["anchorLinks"]["anchorLink" + str(currentanchor) + ""] + '" />\n')
                print('\t\t</navPoint>\n')

                currentanchor += 1

            #print('Added anchor tags to page ' + str(currentpage) + ', ' + data["pages"][currentpage]["fileName"] + '.')

        except KeyError:
            null #Remove this null from final code.
        #print('Skipped page ' + str(currentpage) + ', ' + data["pages"][currentpage]["fileName"] + ' as it had no anchor tags.')
