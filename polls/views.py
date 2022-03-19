# Create your views here. Not a view like an HTML template, but request handler
# request -> response (action)

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'hello.html', { 'name': 'someone'})
