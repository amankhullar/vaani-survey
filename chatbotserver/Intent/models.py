from django.db import models
from django_mysql.models import ListCharField

# Create your models here.
class intent_model(models.Model):
    intent_data = models.CharField(max_length=250)
    training_phrases = ListCharField(
        base_field = models.CharField(max_length=10),
        size=6,
        max_length=(6 * 11)  # 6 * 10 character nominals, plus commas
    )
    responses = models.CharField(max_length=250)

class MyModel(models.Model):
    title = models.CharField(max_length=250)
    text = models.CharField(max_length=250)
    audio = models.FileField(default="myaudio.mp3", blank=True)
    def __str__(self):
        return self.title
    # class Meta:
    #     ordering=['intent_data']
