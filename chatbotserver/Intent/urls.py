from Intent import views
from django.conf.urls import url
from Intent.views import BookListView, HelloWorld, entity_view, establish_connection, get_answer, intent_get, intent_view, list_intents, new_intent

urlpatterns = [
    url(r'^edit_intent/$', intent_view.as_view()),
    url('books/', BookListView.as_view(), name='books'),
    url('view/', entity_view.as_view(), name='view'),
    url(r'^list/$', list_intents.as_view()),
    url(r'add/', new_intent, name="add"),
    url(r'^(?P<id>[\w-]+)/edit/$', HelloWorld.as_view()),
    url(r'get/', intent_get),
    url(r'conn/', establish_connection),
    url(r'getanswer/', get_answer)

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