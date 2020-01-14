from .serializers import updateSerializer
from rest_framework.generics import (CreateAPIView)
from helloworld.models import MyModel

class HelloWorld(CreateAPIView):
	queryset = MyModel.objects.all()
	serializer_class = updateSerializer
	lookup_field = 'id'
