from django.db import models
#from multiselectedfield import MultiSelectField
import re

#Create your models here.
GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)
# DAY_OF_THE_WEEK = {
#    ('1' : ('Monday')),
#    ('2' : ('Tuesday')),
#    ('3' : ('Wednesday')),
#    ('4' : ('Thursday')),
#    ('5' : ('Friday')),
#    ('6' : ('Saturday')),
#    ('7' : ('Sunday')),
# }
class UserManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['email']) < 1:
            errors["email"] = "Email cannot be blank"
        if not EMAIL_REGEX.match(post_data['email']):
            errors["email"] = "Email format not correct"
        if len(post_data['password']) < 6:
            errors["network"] = "Passoword must be at least 6 characters"
        return errors
    def register_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['name']) < 1:
            errors["name"] = "Name cannot be blank"
        if len(post_data['lastname']) < 1:
            errors["lastname"] = "Lastname cannot be blank"
        if len(post_data['email']) < 1:
            errors["email"] = "Email cannot be blank"
        if not EMAIL_REGEX.match(post_data['email']):
            errors["email"] = "Email format not correct"
        if len(post_data['password']) < 6:
            errors["password"] = "Password must be at least 6 characters"
        if len(post_data['confirmpassword']) < 6:
            errors["confirmpassword"] = "Password must be at least 6 characters"
        if post_data['password'] != post_data['confirmpassword']:
            errors["confirmpassword"] = "Password doesnt match"
        return errors

class UserAddress(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    gender = models.IntegerField(choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.OneToOneField(UserAddress, on_delete=models.CASCADE)
    objects = UserManager()

class Business(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.PositiveIntegerField()
    description = models.TextField()
#    work_days = MultiSelectField(choices=DAY_OF_THE_WEEK)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    longitude = models.TextField()
    latitude = models.TextField()

class BusinessHours(models.Model):
    business = models.OneToOneField(Business, related_name="business_hours", on_delete=models.CASCADE)
    work_from_hour = models.TimeField()
    work_to_hour = models.TimeField()
    break_from_hour = models.TimeField()
    break_to_hour = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BusinessDays(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, related_name="business_days", on_delete=models.CASCADE)
    day = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BusinessReviews(models.Model):
    # id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, related_name="business_reviews", on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="review_user", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class BussinesAddress(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    business = models.OneToOneField(Business, related_name="address", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Categories(models.Model):
    name = models.TextField()
    businesses = models.ManyToManyField(Business, related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
