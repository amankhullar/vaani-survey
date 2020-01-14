import polyglot
import pprint
from polyglot.text import Text, Word

# def getPolyglotLocation(userReply):
#     text = Text(userReply, hint_language_code="hi")
#     op = userReply.rstrip() + ','
#     userReplyEntities = {}

#     for e in text.entities:
#         if e.tag == "I-LOC":
#             loc_list = [] 
#             loc = ""
#             for i in e:
#                 loc += i + " "
#             loc_list.append(loc)
#             userReplyEntities["location_mod"] = loc_list
#             userReplyEntities["location"] = e
#     print(userReplyEntities)
#     return userReplyEntities

def getPolyglotLocation(userReply):
    text = Text(userReply, hint_language_code="hi")
    userReplyEntities = {}

    loc_list = [] 
    for e in text.entities:
        if e.tag == "I-LOC":
            loc = " "
            for i in e:
                loc += i + " "
            loc_list.append(loc)
            userReplyEntities["location_mod"] = loc_list
            userReplyEntities["location"] = e
    return userReplyEntities

# userReply = "मैं यूपी में रहता हूं जिला सोनभद्र में आशीष कुमार गुप्ता मेरा नाम है"
# getPolyglotLocation(userReply)