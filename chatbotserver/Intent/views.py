
from .serializers import updateSerializer, hupdateSerializer
from django.views import generic
from rest_framework.generics import (ListCreateAPIView)
from rest_framework.generics import (CreateAPIView)
from Intent.models import intent_model, MyModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.http import HttpResponseRedirect
from .forms import IntentForm
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
import json
from Intent.jsonparser import getNext
from Intent.constructds import *
from Intent.location import getLocation
from Intent.utils import get_name_final, get_loc_final, find_date_final

dataset = []
current_id = ""

class intent_view(ListCreateAPIView):
	queryset = intent_model.objects.all()
	serializer_class = updateSerializer
	lookup_field = 'id'


class BookListView(generic.ListView):
	model = intent_model
	context_object_name = 'intent_model_list'
	queryset = intent_model.objects.all()
	template_name = 'Intent/list_intents.html'

class list_intents(APIView):
	def get(self, request, format=None):
		queryset = intent_model.objects.all()
		serializer = updateSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

class entity_view(generic.ListView):
	model = intent_model.objects.all()
	context_object_name = 'intent_model_list'
	queryset = intent_model.objects.all()
	template_name = 'Intent/list_entities.html'


import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

@api_view(['POST'])
@parser_classes([MultiPartParser])
def intent_get(request):
	# print(request.POST)
	# response_data = "hello"
	global current_id
	global dataset
	obj = intent_model()
	if request.method == 'POST':
		mystr  = request.POST['name1']
		myfile = request.FILES["file1"]
	print(myfile.name)
	data = myfile
	path = default_storage.save('tmp/'+myfile.name, ContentFile(data.read()))
	tmp_file = os.path.join(settings.MEDIA_ROOT, path)

	nextQue, current_id, value = 1,1,1 #getSentance(mystr, current_id, dataset)	
	response_data = nextQue
	# print(response_data)
	return JsonResponse({'message': response_data}, status=200)

#==============================================================================================
# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def get_location(request):
# 	global current_id
# 	global dataset
# 	current_id = 0
# 	dataset = []
# 	obj = intent_model()
# 	if request.method == 'POST':
# 		mystr  = request.POST['name1']
# 		myfile = request.FILES["file1"]
# 	data = myfile
# 	path = default_storage.save('tmp/'+myfile.name, ContentFile(data.read()))
# 	tmp_file = os.path.join(settings.MEDIA_ROOT, path)

# 	response, current_id, value = getLocation(mystr, current_id, dataset)	
# 	response_data = response
# 	print("message decoded : " + str(value))
# 	return JsonResponse({'संदेश': response_data}, status=200)

#==============================================================================================
@api_view(['POST'])
@parser_classes([MultiPartParser])
def get_answer(request):
	global dataset_tree, dataset_entities
	global last_node

	print(last_node["name"])
	next_node = next_question(last_node,dataset_tree)
	try:
		for node in next_node:
			cur_intent = get_system_entity(node)
			obj = intent_model()
			if request.method == 'POST':
				mystr  = request.POST['name1']
				myfile = request.FILES["file1"]
				
			data = myfile
			path = default_storage.save('tmp/'+myfile.name, ContentFile(data.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)


			if cur_intent =="location":
				res = get_loc_final(mystr)
			elif cur_intent =="name":
				res = get_name_final(mystr)
			elif cur_intent =="age":
				res = find_date_final(mystr)
			elif cur_intent==-1:
				res = ""
			else:
				sy = find_synonyms(get_system_entity(node), dataset_entities)
				res = match_synonyms(mystr, sy)
				print("\ncur_intent", cur_intent)
				print("\nnext_node", node)
				print("\nsy", sy)
				print("\nres", res)
			

			response_data = (res)
			next_que = (node["nextQuestion"])
			print("current intent : " +str(cur_intent))
			print("message decoded : " + str(res))
			print("next question : " + str(next_que))

			last_node = node
		return JsonResponse({'संदेश': response_data, 'अगला प्रश्न': next_que}, status=200)
	except:
		print("list index out of range")
		return JsonResponse({'संदेश': "end of survey"}, status=300)


#==============================================================================================
# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def establish_connection(request):
# 	obj = intent_model()
# 	if request.method == 'POST':
# 		survey_name  = request.POST['survey'].rstrip()
# 	global dataset
# 	global current_id
# 	dataset, current_id, followupQuestion = createDataset(survey_name)
# 	response_data = followupQuestion
# 	print(response_data)
# 	return JsonResponse({'message': response_data}, status=200)

#==============================================================================================
dataset_tree = []
dataset_entities = []
last_node = []
@api_view(['POST'])
@parser_classes([MultiPartParser])
def establish_connection(request):
	global dataset_tree, dataset_entities
	global last_node
	
	obj = intent_model()
	if request.method == 'POST':
		survey_name  = request.POST['survey'].rstrip()
	global dataset_tree, dataset_entities
	global last_node
	dataset_tree = createDataset(survey_name)
	dataset_entities = create_entities("Name_Survey")
	start = initial_question(dataset_tree)
	print(start['nextQuestion'])
	last_node = start
	return JsonResponse({'संदेश': start['nextQuestion']}, status=200)
#==============================================================================================

def new_intent(request):
	obj = intent_model() #gets new object
	
	if request.method == 'POST':
		form = IntentForm(request.POST)
		if form.is_valid():
			obj.intent_data = form.cleaned_data['intent_data']
			obj.training_phrases = form.cleaned_data['training_phrases']
			obj.responses = form.cleaned_data['responses']

			obj.save()
			return HttpResponseRedirect('view/')
	else:
		form = IntentForm()
	context = {
		'form' : form, 
		'intent_model_list' : obj
	}
	return render(request, 'Intent/list_intents.html', {'form': form})

class HelloWorld(CreateAPIView):
	queryset = MyModel.objects.all()
	serializer_class = hupdateSerializer
	lookup_field = 'id'


