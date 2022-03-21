# Admin form customization

from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    #choices are shown inline with corresponding question
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Category', {'fields': ['question_category']}),
    ]

    inlines = [ChoiceInline]
    #columns of displayed list of questions:
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    #additional filter for list of questions:
    list_filter = ['pub_date']
    #search capability:
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

