from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home_view(request):
    return HttpResponse('Hello World!')

@csrf_exempt
def webhook(request):
    # build a request object
    req = json.loads(request.body)
    # get action from json
    action = req.get('queryResult').get('action')
    # return a fulfillment message
    fulfillmentText = {'fulfillmentText': 'This is Django test response from webhook.'}
    # return response
    return JsonResponse(fulfillmentText, safe=False)