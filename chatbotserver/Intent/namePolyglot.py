import polyglot
import pprint
from polyglot.text import Text, Word

def getPolyglotName(userReply):
    text = Text(userReply, hint_language_code="hi")
    userReplyEntities = {}

    loc_list = [] 
    for e in text.entities:
        if e.tag == "I-PER":
            loc = " "
            for i in e:
                loc += i + " "
            loc_list.append(loc)
            userReplyEntities["person_mod"] = loc_list
            userReplyEntities["person"] = e
    return userReplyEntities

# userReply = "मैं यूपी में रहता हूं जिला सोनभद्र में आशीष कुमार गुप्ता मेरा नाम है"
# print(getPolyglotName(userReply))