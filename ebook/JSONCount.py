import json
from collections import OrderedDict

with open("metadata.json") as json_file:
    data = json.load((json_file), object_pairs_hook=OrderedDict) #For some reason the order is randomised, this preserves the order.

print len(data["pages"])
