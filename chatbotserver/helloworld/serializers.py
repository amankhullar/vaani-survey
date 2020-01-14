from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
)
from helloworld.models import MyModel

class updateSerializer(ModelSerializer):
	class Meta:
		model = MyModel
		fields = [
			'title',
			'text',
			'audio'
		]
