# Create your models here. 
# With these classes, django is able to create a python DB-access API

import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_category = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

    #methods
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    #methods
    def __str__(self):
        return self.choice_text


