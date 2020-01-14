# -*- coding: utf-8 -*-

import json
import glob
import os
import pprint
import difflib

path = '/Himanshu_Survey/intents/'
# os.chdir("../")
global_path = os.getcwd()+path

class Test(object):
    # Loads data of any json file
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

def getIntent(path):
    # Gets intent from file name : the first part of filename contains name of intent eg getName, Hello
    return path.split('_')[0]

def constructDict(mydict):
    # get the possible text datafields from all of 
    for traindir in os.listdir(global_path):
        with open(global_path+traindir, 'r') as f:
            json_data = json.load(f)
            if(traindir.find('usersays')==-1):
                # print(json_data["id"])
                count = 0
            else:
                for data in json_data:
                    sentance = ""
                    for d in data['data']:
                        sentance += d['text']
                    mydict[sentance] = getIntent(traindir)


# pp.pprint(mydict)
mydict = {}
constructDict(mydict)
pp = pprint.PrettyPrinter(indent=4)
text = "I Himanshu"
nearest_text = difflib.get_close_matches(text, mydict.keys(), 1, 0.8)
# print(text, nearest_text)
# print(mydict[nearest_text[0]])

def getResponse(intentName):
    traindir = intentName+".json"
    with open(global_path+traindir, 'r') as f:
        json_data = json.load(f)
        response = json_data["responses"][0]["messages"][0]["speech"]
        return response

def getReprompt(intentName):
    traindir = intentName+".json"
    with open(global_path+traindir, 'r') as f:
        json_data = json.load(f)
        prompt = json_data["responses"][0]["parameters"][0]["prompts"][0]["value"]
        return prompt

response = getResponse(mydict[nearest_text[0]])
print(response)

def getNext(text):
    mydict = {}
    constructDict(mydict)
    nearest_text = difflib.get_close_matches(text, mydict.keys(), 1, 0.8)
    if(not nearest_text):
        response = "Sorry couldn't get you"
    else :
        response = getResponse(mydict[nearest_text[0]])
    return response

#### Hindi Demo
# mylist = ["ट्रैफिक पुलिसकर्मियों", "वेस्ट जिला", "जीएसटी:","दिल्ली","शिकायत"]
# text = "ट्रैफिक पुलिस"
# nearest_text = difflib.get_close_matches(text, mylist, 1, 0.6)
# print text.decode('utf-8')
# print nearest_text[0].decode('utf-8')


    # tif = sorted(glob.glob(traindir+'*.png'))
    # tempy = np.array(pd.read_csv(traindir+'rew.csv', header=None)).astype(int)
    # tvalues = range(7, len(tempy))
    # positivets = [t for t in tvalues if tempy[t-1]==1]
    # negativets = [t for t in tvalues if tempy[t-1]==0]
    # negativets = sample(negativets, len(positivets)*3)
    # ts = positivets + negativets
    # shuffle(ts)
    # ind0 = np.array([np.array([t-7,t-6,t-5,t-4,t-3,t-2,t-1]) for t in ts])
    # ind1 = np.array([np.delete(trainingx, np.random.randint(6), axis=0) for trainingx in ind0])
    # ind2 = np.array([np.delete(trainingx, np.random.randint(5), axis=0) for trainingx in ind1])
    # i = ind2
    # drop2x = pd.DataFrame([(tif[i[0]],tif[i[1]],tif[i[2]],tif[i[3]], tif[i[4]], int(tempy[i[4]])) for i in ind2])
    # if(traindir==train_image_folders[0]):
    #     trainx = drop2x
    # else:
    #     trainx = trainx.append(drop2x)

#
#
#

#
