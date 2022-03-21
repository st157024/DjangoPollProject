# Model classes 
# With these classes, django is able to create a python DB-access API

import datetime
from email.policy import default
from xmlrpc.client import boolean

from django.db import models
from django.utils import timezone
from django.contrib import admin



class Category(models.Model):
    #fields
    name = models.CharField(max_length=100, default='')
    #slug for readable url paths
    slug = models.SlugField()

    #methods
    def __str__(self):
        return self.name


class Question(models.Model):
    #fields
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    #category as foreign key
    """
    With the way category is used in this project, one-to-one mapping 
    would suffice since every question is only given one category.
    This could be extended with multiple categories and sub-categories though, 
    hence ForeignKey is used here.
    """
    question_category = models.ForeignKey(Category, null=True, blank=True, default='', on_delete=models.SET_DEFAULT)

    #methods
    def __str__(self):
        return self.question_text

    #change column header in admin page
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    


class Choice(models.Model):
    #fields
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    #methods
    def __str__(self):
        return self.choice_text


