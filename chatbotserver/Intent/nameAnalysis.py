# -*- coding: utf-8 -*-
import pandas as pd
import re
import os
from namePolyglot import getPolyglotName

def getName(mystr):
    nameEntities = getPolyglotName(mystr)
    if(bool(nameEntities)):
        entity = nameEntities["person_mod"]
        return entity
    else:
        entity = "n"
        return entity

filename = "dataset.csv"
transcriptdf = pd.read_csv(filename)
del transcriptdf['locations']
transcript = transcriptdf["Transcript"].tolist()

n = len(transcript)
polyglotName = [None]*n


for i in range(n):
    instance = transcript[i]
    polyglotName[i] = getName(instance) #prints location identified as well
    print("====================")

outdf = pd.DataFrame(polyglotName, transcript[:n])
outdf.to_csv('polyglotName.csv')


# userReply = "मैं यूपी में रहता हूं जिला सोनभद्र में आशीष कुमार गुप्ता मेरा नाम है"
# print(getName(userReply, 0, 0))