## -*- coding: utf-8 -*-


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


def reask_fallback(id):
    for traindir in os.listdir(global_intents_path):
        with open(global_intents_path+traindir, 'r') as f:
            # print("reask_fallback", traindir)
            if(traindir.find('usersays')!=-1):
                count = 0
            else:
                with open(global_intents_path+traindir, 'r') as mainfile:
                    json_main_data = json.load(mainfile)
                    if 'parentId' in json_main_data:
                        # print("Entered")
                        if(json_main_data['parentId']==id and json_main_data['fallbackIntent']==True):
                            return json_main_data['responses'][0]['messages'][0]['speech']
    return -1



def createDataset(survey_name):
    setGlobalPaths(survey_name)
    dataset = []
    current_id, followupQuestion = "", ""
    for traindir in os.listdir(global_intents_path):
        # print("In line", traindir)

        with open(global_intents_path+traindir, 'r') as f:
            json_data = json.load(f)
            if(traindir.find('usersays')==-1):
                count = 0
            else:
                tmp_dataset = {}
                with open(global_intents_path+getIntent(traindir)+'.json', 'r') as mainfile:
                    json_main_data = json.load(mainfile)
                    tmp_dataset['name'] = traindir
                    tmp_dataset['id'] = json_main_data['id'] 
                    if traindir.find('Hello.json') :
                        current_id = json_main_data['id']
                        followupQuestion = json_main_data['responses'][0]['messages'][0]['speech']
                    if 'parentId' in json_main_data:
                        #if parent is there both root and parent shall be there
                        tmp_dataset['parentId'] = json_main_data['parentId']
                        tmp_dataset['rootId'] = json_main_data['rootParentId']
                    # if json_main_data['responses'][0]['parameters'] != []:
                        # tmp_dataset['last_question']= bool(False)
                    tmp_dataset['reaskQuestion'] = reask_fallback(json_main_data['id'])

                    tmp_dataset['nextQuestion'] = json_main_data['responses'][0]['messages'][0]['speech'] 
                    # else:

                        # tmp_dataset['last_question']= bool(True)
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
                #print(dataset)#.decode('utf-8') 
    # for element in dataset:
    #     print("printing final")
    #     pprint.pprint(element)
    #     print(element['nextQuestion'])
    #     print(element['reaskQuestion'])
    return dataset


def create_entities(survey_name):
    setGlobalPaths(survey_name)
    dataset = []
    for traindir in os.listdir(global_entities_path):
        # print("In line", traindir)

        with open(global_entities_path+traindir, 'r') as f:
            json_data = json.load(f)
            if(traindir.find('_entries_')!=-1):
                with open(global_entities_path+traindir, 'r') as mainfile:
                    json_main_data = json.load(mainfile)
                    entities = {}
                    with open(global_entities_path+traindir.split('_')[0]+'.json', 'r') as p:
                        tmp = json.load(p)
                        entities['name'] = tmp['name']
                        entities['entries'] =[]
                    for element in json_main_data:
                        tmp_dataset = {}
                        tmp_dataset['value'] = element['value']
                        tmp_dataset['synonyms'] = element['synonyms'] 
                        entities['entries'].append(tmp_dataset)
                    dataset.append(entities)
    return dataset
      

# def searchEntity(tmpstr, json_data):
#     for value in json_data:
#         for text in value['synonyms']:
#             # print(text)
#             if tmpstr.startswith(text.lower()):
#                 return text, value['value']
#     return "notfound", 404
#         # pprint.pprint(intent['responses'])


# def getSentance(mystr, current_id, dataset):
#     for intent in dataset:
#         if 'parentId' in intent and intent['parentId'] == current_id:
#             sentance_list = intent['responses']
#             for sentance in sentance_list:
#                 tmpstr = mystr
#                 for word in sentance:
#                     # print(tmpstr)
#                     if(word['userDefined'] == False):
#                         text = word['text']
#                         if tmpstr.startswith(text):
#                             tmpstr = tmpstr[len(text):]
#                         else : 
#                             break
#                     else:
#                         with open(global_entities_path + word['entity']+'_entries_en.json', 'r') as f:
#                             json_data = json.load(f)
#                             text, value = searchEntity(tmpstr, json_data)
#                             if text != "notfound":
#                                 tmpstr = tmpstr[len(text):]
#                 if tmpstr=="":
#                     #string matched with sentance
#                     return intent['nextQuestion'], intent['id'], value
#             return intent['reaskQuestion'], current_id, 404


# tree = createDataset("Survey_people")

# pprint.pprint(tree)
# for element in tree:
#     if not 'parentId' in element:
#         print("found")
#         pprint.pprint(element)
#         print(element['name'])



def initial_question(dt):
    for element in dt:
        if not 'parentId' in element:
            # print("names ",element['name'])
            return element
    return -1

def child_node(id, node, dt):
    l=[]
    for element in dt:
        if 'parentId' in element:
            # print("names ",element['name'])
            if element['parentId']==id:
                l.append(element)

    return l



def next_question(node, dt):
    element = child_node(node['id'],node,dt)
    return element

def get_system_entity(node):
    print("responses", node['responses'])
    for element in node['responses']:
        for word in element:
            if word['userDefined']==True:
                if(word['entity']=="sys.given-name"):
                    return "name"
                elif(word['entity']=="sys.location"):
                    return "location"
                elif(word['entity']=="sys.age"):
                    return "age"
                else:
                    return word['entity']
    return -1

def match_response(st,node):
    for response in node['responses']:
        flag = 0
        for text in responses:
            if text['text'] in st:
                flag = 1
            else:
                flag = 0
                break
        if (flag == 1):
            return 1
    return -1




def find_synonyms(nm, table):
    for element in table:
        if element['name'] == nm:
            return element['entries']

def match_synonyms(st,entries):
    for lt in entries:
        for sy in lt['synonyms']:
            if (sy in st):
                return lt['value']
    return -1





# tree = createDataset("../Name_Survey")
# similar=create_entities("../Name_Survey")

# # pprint.pprint(initial_question(tree))
# start = initial_question(tree)
# pprint.pprint(start['name'])

# next_node = next_question(start,tree)
# # pprint.pprint(next_node[0])
# print(get_system_entity(next_node[0]))
# print("1",next_node[0]['name'])
# print(next_node[0])


# next_node = next_question(next_node[0],tree)
# print(get_system_entity(next_node[0]))
# print("2",next_node[0]['name'])


# next_node = next_question(next_node[0],tree)
# print(get_system_entity(next_node[0]))
# print("3",next_node[0]['name'])


# next_node = next_question(next_node[0],tree)
# print(get_system_entity(next_node[0]))
# print("4",next_node[0]['name'])
# print(next_node[0]['responses'])
# # print(find_synonyms(get_system_entity(next_node[0]), similar))
# sy = find_synonyms(get_system_entity(next_node[0]), similar)
# st = "Gender-female"
# print(match_synonyms(st,sy))


# next_node = next_question(next_node[0],tree)
# print(get_system_entity(next_node[0]))
# print("5",next_node[0]['name'])
# sy = find_synonyms(get_system_entity(next_node[0]), similar)
# st = "Nhi"
# print(match_synonyms(st,sy))

# next_node = next_question(next_node[0],tree)
# print(next_node)
