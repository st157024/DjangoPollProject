# Create your views here. Not a view like an HTML template, but request handler
# request -> response (action)


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    #override auto-generated template name to use existing template:
    template_name= 'polls/index.html'
    #override auto-generated context variable to use existing one:
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        #return the last 5 published questions, not including future ones
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    #override auto-generated template name
    template_name = 'polls/detail.html'

    def get_queryset(self):
        #exclude any question that aren't published yet
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    #override auto-generated template name
    template_name = 'polls/results.html'



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