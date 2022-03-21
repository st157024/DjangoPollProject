# View creation file. 
'''
Not a view like an HTML template, but a request handler
request -> response (action)
'''


from re import template
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from .models import Question, Choice, Category

# list of recently published questions 
class IndexView(generic.ListView):
    #override auto-generated template name to use existing template:
    template_name= 'polls/index.html'
    #override auto-generated context variable to use existing one:
    context_object_name = 'latest_question_list'


    #method for category list as additional context
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.order_by('name')
        return context



    def get_queryset(self):
        #return the last 8 published questions, not including future ones
        #lte => 'less than or equal
        """
        Using the annotate function to get count of choices associated with a question 
        and filter questions without sufficient choice count
        """
        return Question.objects.annotate(number_of_choices=Count('choice')).filter(
            number_of_choices__gte=2
            ).filter(
            pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:8]


#detailed view for a chosen question
class DetailView(generic.DetailView):
    model = Question
    #override auto-generated template name
    template_name = 'polls/detail.html'

    def get_queryset(self):
        #exclude any question that aren't published yet
        """
        Access to questions with insufficient amount of choices has to be prevented through url guessing as well
        """
        return Question.objects.annotate(number_of_choices=Count('choice')).filter(
            number_of_choices__gte=2
            ).filter(
            pub_date__lte=timezone.now())
        #return Question.objects.filter(pub_date__lte=timezone.now())

#results view for a chosen question (votes)
class ResultsView(generic.DetailView):
    model = Question
    #override auto-generated template name
    template_name = 'polls/results.html'


#voting handler
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        #selected choice contains id of voted choice, accessed with name 'choice'
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplaying question voting form in case missing vote
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        #using HttpResponseRedirect prevents data being posted twice by hitting back button
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


#category view
"""
This takes a request and a slug as arguments.
With the slug, questions can be filtered after category and only questions belonging 
into the desired category are given to the template as context
"""
def show_category(request, slug):
    category_question_list = Question.objects.filter(question_category__slug=slug)
    context = {'category_question_list': category_question_list, 'category_name': slug}
    return render(request, 'polls/category.html', context)