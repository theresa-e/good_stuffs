from __future__ import unicode_literals
from django.db import models
import bcrypt
import re #regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class ErrorManager(models.Manager):
    def basic_validator(self, requestPOST):
        errors = {}
        # Check if the username is already in our db.
        user_list = User.objects.filter(email=requestPOST['email'])
        if len(requestPOST['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters long."
        if len(requestPOST['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters long."
        if len(requestPOST['email']) < 2:
            errors['email'] = "Email required for registration."
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['email_format'] = "Please enter a valid email."
        if len(requestPOST['password']) < 8:
            errors['password_len'] = "Password must be at least 8 characters long."
        if requestPOST['password'] != requestPOST['confirm_password']:
            errors['password_match'] = "Please confirm password before registering, they do not match."
        if len(user_list) > 0:
            errors['existing_user'] = "That email is already associated with an account."
        return errors

    def create_user(self, requestPOST):
        all_users = User.objects.all()
        # Determine what user_type 
        if len(all_users) > 0:
            user_type = 0
        else:
            user_type = 1
        hash = bcrypt.hashpw(requestPOST['password'].encode(), bcrypt.gensalt())
        print(hash)
        return User.objects.create(first_name=requestPOST['first_name'], last_name=requestPOST['last_name'], email=requestPOST['email'], pw_hash=hash, user_type=user_type)

    def login_validator(self, requestPOST):
        errors = {}
        user_list = User.objects.filter(email=requestPOST['login_email'])
        print('USER LIST:', user_list)
        if len(requestPOST['login_email']) < 1:
            errors['login_email'] = "Login email cannot be blank."
        if not EMAIL_REGEX.match(requestPOST['login_email']):
            errors['login_format'] = "Please enter a valid email."
        if not len(user_list):
            errors['email_error'] = "This email is not valid."
        elif len(user_list) > 0:
            user = User.objects.get(email=requestPOST['login_email'])
            hash1 = bcrypt.hashpw('test'.encode(), bcrypt.gensalt())
            if not bcrypt.checkpw(requestPOST['login_password'].encode(), user.pw_hash.encode()):
                errors['pw_error'] = "You could not be logged in."
            else:
                print('-'*30+'> ', 'Password is correct!')
                print('-'*30+'> ', 'User logged in successfully. ')
        return errors

    def update_info_validator(self, requestPOST):
        errors = {}
        user = User.objects.get(id=requestPOST['userid'])
        email_check = User.objects.filter(email=requestPOST['email'])
        if len(requestPOST['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters long."
        if len(requestPOST['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters long."
        if len(requestPOST['email']) < 2:
            errors['email'] = "Email required for registration."
        if not EMAIL_REGEX.match(requestPOST['email']):
            errors['email_format'] = "Please enter a valid email."
        if len(email_check) > 0:
            if requestPOST['email'] == user.email:
                pass 
                # User didn't change email
            else:
                errors['email_exists'] = "The email you entered is already in use. Please enter a different one."
        return errors
        

    def quote_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['quote']) < 10:
            errors['quote_len'] = "Provide the entire quote."
        if len(requestPOST['author']) < 3:
            errors['author_len'] = "Enter the author's entire name."
        if not len(errors):
            user = User.objects.get(id=requestPOST['userid'])
            new_quote = Quote.objects.create(quote=requestPOST['quote'], author=requestPOST['author'], uploaded_by=user)
        return errors

    def product_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['name']) < 1:
            errors['name_len'] = "Product must have a name."
        if len(requestPOST['description']) < 1:
            errors['description'] = "Product must have a description."
        if len(requestPOST['price']) < 1:
            errors['price'] = "Product must have a price."
        if not len(errors):
            new_product = Product.objects.create(name = requestPOST['name'], description = requestPOST['description'], price = requestPOST['price'], category = requestPOST['category'], inventory = requestPOST['inventory'])
            new_product.save()
        return errors

class Product(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    inventory = models.IntegerField(default=0)
    quantity_sold = models.IntegerField(default=0)
    category = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=200)
    objects = ErrorManager()

    def __repr__(self): 
        return "<Product object: {} {} {} {} {}>".format(self.name, self.description, self.price, self.inventory, self.quantity_sold)

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=15)
    user_type = models.IntegerField()
    pw_hash = models.CharField(max_length=200)
    orders = models.IntegerField(default=0) # orders the customer has placed
    cart = models.ManyToManyField(Product, related_name="products_in_cart") # current items in customer's cart
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ErrorManager()

    def __repr__(self): 
        return "<User object: {} {} {} {}>".format(self.first_name, self.last_name, self.email, self.user_type)


class Address(models.Model):
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    total = models.IntegerField()
    buyer = models.ForeignKey(User, related_name="ordered_by")
    items = models.ManyToManyField(Product, related_name="products_ordered") # list of products ordered
    ship_to = models.ForeignKey(Address, related_name="shipto_address")
    bill_to = models.ForeignKey(Address, related_name="billto_address")
    status = models.CharField(max_length=10) # will change when order ships and is delivered.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)