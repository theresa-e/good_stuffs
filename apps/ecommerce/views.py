from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    print('User navigated to main page.')
    return render(request, 'ecommerce/index.html')

def categories(request):
    print('User navigated to the categories page.')
    context = {
        'all_products' : Product.objects.all()
    }
    return render(request, 'ecommerce/categories.html', context)

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
        if 'customer_cart' not in request.session:
            request.session['customer_cart'] = {}
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
        if 'user_type' not in request.session:
            request.session['user_type'] = user.user_type
        request.session['user_type'] = user.user_type
        if 'customer_cart' not in request.session:
            request.session['customer_cart'] = {}
        print('REQUEST.SESSION: ', request.session)
        # Create the new user!
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

def account_info(request, id):
    context = {
        'user' : User.objects.get(id=id)
    }
    return render(request, 'ecommerce/acct-info.html', context)

def add_to_cart(request):
    cart = request.session.get('cart', {})
    print('@@@@@@', cart)
    if request.POST['product_id'] in cart:
        cart[request.POST['product_id']] = int(cart[request.POST['product_id']]) + int(request.POST['quantity'])
    else:
        cart[request.POST['product_id']] = int(request.POST['quantity'])
    request.session['cart'] = cart

    total_items = 0
    for i in cart:
        total_items += cart[i]
    request.session['total_items'] = total_items
    return redirect('/categories',)

def visit_cart(request):
    return render(request, 'ecommerce/cart.html')

def orders(request):
    print('Admin is viewing all orders.')
    if request.session['user_type'] != 1:
        print('User without admin access tried to visit /products.')
        return redirect('/')
    return render(request, 'ecommerce/orders.html')

def users(request):
    print('Admin is viewing all users')
    context = {
        'all_users' : User.objects.all()
    }
    return render(request, 'ecommerce/users.html', context)

def edit_user(request, id):
    user = User.objects.filter(id=id).first()
    user.user_type = request.POST['account-level']
    user.save()
    return redirect('/admin/users')

def products(request):
    print('Admin is viewing all products.')
    print('------ REQUEST.SESSION', request.session)
    if request.session['user_type'] != 1:
        print('User without admin access tried to visit /products.')
        return redirect('/')
    context = {
        'all_products' : Product.objects.all()
    }
    return render(request, 'ecommerce/products.html', context)

def add_product(request):
    print('Admin is adding a product.')
    if request.session['user_type'] != 1:
        print('User without admin access tried to visit /products.')
        return redirect('/')
    else:
        return render(request, 'ecommerce/add-product.html')

def process_product(request):
    print('Admin is creating a new product.')
    errors = Product.objects.product_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/admin/add-product')
    else:
        return redirect('/admin/products')

def delete_product(request, id):
    product = Product.objects.filter(id=id).first()
    product.delete()
    return redirect('/admin/products')

def edit_product(request, id):
    context = {
        'edit_product' : Product.objects.filter(id=id).first()
    }
    return render(request, 'ecommerce/edit-product.html', context)

def process_edit(request, id):
    product = Product.objects.filter(id=id).first()
    product.name = request.POST['name']
    product.description = request.POST['description']
    product.price = request.POST['price']
    product.cateogry = request.POST['category']
    product.inventory = request.POST['inventory']
    product.save()
    return redirect('/admin/products')

def customers(request):
    print('Admin is viewing all customers.')
    if not request.session['user_type'] == 1:
        print('User without admin access tried to visit /products.')
        return redirect('/')
    return render(request, 'ecommerce/customers.html')


def logout(request):
    request.session.flush()
    return redirect('/')