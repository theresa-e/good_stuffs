from django.shortcuts import render, HttpResponse, redirect

def index(request):
    response = "AYOO HOLLA MAMA"
    return HttpResponse(response)