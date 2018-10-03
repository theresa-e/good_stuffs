from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    print('User navigated to main page.')
    return render(request, 'ecommerce/index.html')

def categories(request):
    print('User navigated to the categories page.')
    return render(request, 'ecommerce/categories.html')

def login(request):
    print('User navigated to the login page.')
    return render(request, 'ecommerce/login.html')

def process_login(request):
    print('User tried to login.')
    # Save login email to form input
    if 'login_email' not in request.session:
        request.session['login_email'] = request.POST['login_email']
    request.session['login_email'] = request.POST['login_email']

    # Validate user input (form must be complete and filled out)
    # Check to see if user exists and password is valid.
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')

    # If there are no errors, then this is a valid user!
    # Save their info to session and redirect them to product page.
    else:
        user = User.objects.get(email=request.POST['login_email'])    
        if 'first_name' not in request.session:
            request.session['first_name'] = user.first_name 
        request.session['first_name'] = user.first_name 
        if 'welcome_msg' not in request.session:
            request.session['welcome_msg'] = 'You\'ve logged in successfully.'
        request.session['welcome_msg'] = 'You\'ve logged in successfully.'
        if 'userid' not in request.session:
            request.session['userid'] = user.id
        request.session['userid'] = user.id
        if 'user_type' not in request.session:
            request.session['user_type'] = user.user_type
        request.session['user_type'] = user.user_type        
        return redirect('/categories')
def process_new_user(request):
    print('-'*30+'> ' 'The registration form was submitted.')
    errors = User.objects.basic_validator(request.POST)

    # Validate form, check if email already exists in database.
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print('-'*30+'> ', 'Errors: ', errors)
        return redirect('/create-acct')
    else:
        # Save user info to form input
        if 'first_name' not in request.session:
            request.session['first_name'] = request.POST['first_name']  
        request.session['first_name'] = request.POST['first_name']  
        if 'last_name' not in request.session:
            request.session['last_name'] = request.POST['last_name']
        request.session['last_name'] = request.POST['last_name']
        if 'email' not in request.session:
            request.session['email'] = request.POST['email']
        request.session['email'] = request.POST['email']
        User.objects.create_user(request.POST)

        # Save new user ID in session
        user = User.objects.get(email=request.POST['email'])
        if 'userid' not in request.session:
            request.session['userid'] = user.id
        print('-'*30+'> ', 'A new user was created!')
        print('-'*30+'> ', 'Current users:\n', User.objects.all())
        return redirect('/')

def create_acct(request):
    print('User navigated to the login page.')
    return render(request, 'ecommerce/create-acct.html')

def account_info(request):
    context = {
        'user' : User.objects.get(id=request.session['userid'])
    }
    return render(request, '/acct-info')

def admin(request):
    print('Admin is visiting dashboard')
    return render(request, 'ecommerce/admin.html')

def logout(request):
    request.session.flush()
    return redirect('/')