from django.shortcuts import render, HttpResponse, redirect

def index(request):
    print('User navigated to main page.')
    return render(request, 'ecommerce/index.html')

def categories(request):
    print('User navigated to the categories page.')
    return render(request, 'ecommerce/categories.html')

def login(request):
    print('User navigated to the login page.')
    return render(request, 'ecommerce/login.html')

def create_acct(request):
    print('User navigated to the login page.')
    return render(request, 'ecommerce/create-acct.html')
