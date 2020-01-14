from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
)
from Intent.models import intent_model
from helloworld.models import MyModel

class updateSerializer(ModelSerializer):
	class Meta:
		model = intent_model
		fields = [
			'responses'
		]


class hupdateSerializer(ModelSerializer):
	class Meta:
		model = MyModel
		fields = [
			'title',
			'text',
			'audio'
		]


# from rest_framework import serializers
# from rest_framework.serializers import (
# 	ModelSerializer,
# )
# from Intent.models import intent_model

# class updateSerializer(serializers.Serializer):
# 	intent_data = serializers.CharField(max_length=250)
# 	def create(self, validated_data):
# 		return intent_model.objects.create(**validated_data)
	
# 	def update(self, instance, validated_data):
# 		instance.intent_data = validated_data.get('intent_data', instance.intent_data)
# 		instance.save
# 		return instance

