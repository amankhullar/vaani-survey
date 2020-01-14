# -*- coding: utf-8 -*-
import pandas as pd
import re
import os
from Intent.namePolyglot import getPolyglotName

def getName(mystr, current_id, dataset):
    nameEntities = getPolyglotName(mystr)
    if(bool(nameEntities)):
        entities = nameEntities["person_mod"]
        return "PolyGlot " + str(entities), current_id, 300

    else:
        return "कृपया अपना नाम दोहराए ", current_id, 300



# userReply = "मैं यूपी में रहता हूं जिला सोनभद्र में आशीष कुमार गुप्ता मेरा नाम है"
# print(getName(userReply, 0, 0))