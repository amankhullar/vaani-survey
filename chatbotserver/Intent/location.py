# -*- coding: utf-8 -*-
import pandas as pd
import re
import os
from Intent.locationPolyglot import getPolyglotLocation
from Intent.locationEntityMatch import getEntityLocation

def getLocation(mystr, current_id, dataset):
# def getLocation(mystr):
    locationEntities = getPolyglotLocation(mystr)
    if(bool(locationEntities)):
        entities = locationEntities["location_mod"]
        loc = []
        for entity in entities:
            curlocs = getEntityLocation(entity)
            for curloc in curlocs:
                loc.append(curloc)
        print(loc)
        stat, S, D, SD, _ = loc[0]
        if stat == -1:
            return "PolyGlot " + str(entities), current_id, 300
        else:
            return "PolyGlot + Direct" + str(loc), "100", loc
    else:
        entity = mystr
        loc = getEntityLocation(entity)
        stat, S, D, SD, _ = loc
        if stat == -1:
            return "कृपया अपना जगह दोहराए ", current_id, 300
        else:
            return "Direct" + str(loc), "100", loc
