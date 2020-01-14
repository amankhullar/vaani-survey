from django.db import models

class MyModel(models.Model):
	title = models.CharField(max_length=250)
	text = models.CharField(max_length=250)
	audio = models.FileField(default="myaudio.mp3", blank=True)
	def __str__(self):
		return self.title