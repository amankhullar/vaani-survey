import json
import glob
import os
import pprint
import difflib



# os.chdir("../../")


class Test(object):
    # Loads data of any json file
    def __init__(self, data):
	    self.__dict__ = json.loads(data)


def getIntent(path):
    # Gets intent from file name : the first part of filename contains name of intent eg getName, Hello
    return path.split('_')[0]

global_intents_path = ""
global_entities_path = ""

def setGlobalPaths(survey_name):
    path = '/'+survey_name+'/intents/'
    global global_intents_path 
    global_intents_path = os.getcwd()+path
    entitypath = '/'+survey_name+'/entities/'
    global global_entities_path 
    global_entities_path = os.getcwd()+entitypath

def createDataset(survey_name):
    setGlobalPaths(survey_name)
    dataset = []
    current_id, followupQuestion = "", ""
    for traindir in os.listdir(global_intents_path):
        with open(global_intents_path+traindir, 'r') as f:
            json_data = json.load(f)
            if(traindir.find('usersays')==-1):
                count = 0
            else:
                tmp_dataset = {}
                with open(global_intents_path+getIntent(traindir)+'.json', 'r') as mainfile:
                    json_main_data = json.load(mainfile)
                    tmp_dataset['id'] = json_main_data['id']
                    if traindir.find('Hello.json') :
                        current_id = json_main_data['id']
                        followupQuestion = json_main_data['responses'][0]['messages'][0]['speech']
                    if 'parentId' in json_main_data:
                        #if parent is there both root and parent shall be there
                        tmp_dataset['parentId'] = json_main_data['parentId']
                        tmp_dataset['rootId'] = json_main_data['rootParentId']
                    if json_main_data['responses'][0]['parameters'] != []:
                        tmp_dataset['reaskQuestion'] = json_main_data['responses'][0]['parameters'][0]['prompts'][0]['value']
                        tmp_dataset['nextQuestion'] = json_main_data['responses'][0]['messages'][0]['speech']
                # print tmp_dataset
                tmp_responselist = []
                for data in json_data:
                    tmp_response = []
                    for d in data['data']:
                        tmp_response_data = {}
                        tmp_response_data['text'] = d['text']
                        if d['userDefined']:
                            tmp_response_data['userDefined'] = d['userDefined']
                            tmp_response_data['entity'] = d['meta'][1:]
                        else:
                            tmp_response_data['userDefined'] = d['userDefined']
                        tmp_response.append(tmp_response_data)
                    tmp_responselist.append(tmp_response)
                tmp_dataset['responses'] = tmp_responselist
                dataset.append(tmp_dataset)
    return dataset, current_id, followupQuestion

def searchEntity(tmpstr, json_data):
    for value in json_data:
        for text in value['synonyms']:
            # print(text)
            if tmpstr.startswith(text.lower()):
                return text, value['value']
    return "notfound", 404
        # pprint.pprint(intent['responses'])


def getSentance(mystr, current_id, dataset):
    for intent in dataset:
        if 'parentId' in intent and intent['parentId'] == current_id:
            sentance_list = intent['responses']
            for sentance in sentance_list:
                tmpstr = mystr
                for word in sentance:
                    # print(tmpstr)
                    if(word['userDefined'] == False):
                        text = word['text']
                        if tmpstr.startswith(text):
                            tmpstr = tmpstr[len(text):]
                        else : 
                            break
                    else:
                        with open(global_entities_path + word['entity']+'_entries_en.json', 'r') as f:
                            json_data = json.load(f)
                            text, value = searchEntity(tmpstr, json_data)
                            if text != "notfound":
                                tmpstr = tmpstr[len(text):]
                if tmpstr=="":
                    #string matched with sentance
                    return intent['nextQuestion'], intent['id'], value
            return intent['reaskQuestion'], current_id, 404