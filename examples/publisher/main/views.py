# Create your views here.
from django_kombu.client import publish
from django.shortcuts import render_to_response,render, redirect
from django.http import HttpResponse

def home1(request):
    for x in xrange(100000):
        publish('test.home1', {'home1':x})
    return HttpResponse('home1')

def home2(request):
    for x in xrange(10000):
        publish('test.home2', {'home2':x})
    return HttpResponse('home2')

def home3(request):
    for x in xrange(10000):
        publish('test.home3', {'home3':x})
    return HttpResponse('home3')
