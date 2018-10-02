from django.shortcuts import render, HttpResponse, redirect

def index(request):
    print('User navigated to main page.')
    return render(request, 'ecommerce/index.html')

def categories(request):
    print('User navigated to the categories page.')
    return render(request, 'ecommerce/categories.html')