from Intent import views
from django.conf.urls import url
from Intent.views import (
    intent_view,
    BookListView,
    list_intents,
    new_intent,
    entity_view,
    HelloWorld,
    intent_get,
    establish_connection,
    get_location
    )

urlpatterns = [
    url(r'^edit_intent/$', intent_view.as_view()),
    url('books/', BookListView.as_view(), name='books'),
    url('view/', entity_view.as_view(), name='view'),
    url(r'^list/$', list_intents.as_view()),
    url(r'add/', new_intent, name="add"),
    url(r'^(?P<id>[\w-]+)/edit/$', HelloWorld.as_view()),
    url(r'get/', intent_get),
    url(r'conn/', establish_connection),
    url(r'getlocation/', get_location)
]



# dataset, current_id, followupQuestion = createDataset("sample-survey-1")
# 	print(current_id, followupQuestion)
# 	# followupQuestion, current_id, value = getSentance("hi", current_id, dataset)

# 	# pprint.pprint(dataset)

# 	mystr = "I am boy"
# 	nextQue, current_id, value = getSentance(mystr, current_id, dataset)
# 	print(mystr)
# 	print(nextQue, value)

# 	mystr = "I am 21 years old"
# 	pprint.pprint(getSentance(mystr, current_id, dataset))