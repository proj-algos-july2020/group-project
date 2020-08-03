from django.shortcuts import render, redirect
from .models import User, Business, UserAddress, BusinessHours, BusinessDays, BussinesAddress, Categories, BusinessReviews
import bcrypt
import string
import random
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#Create your views here.
def l_page(request):
    return render(request, "main.html")

def index(request):
    if request.method == 'GET':
        categories = Categories.objects.all()
        context = {
            'categories' : categories
        }
        return render(request, 'index.html', context)

def category(request, id):
    category = Categories.objects.get(id = id)
    businesses = category.businesses.all()
    context = {
        'category' : category,
        'businesses' : businesses
    }
    return render(request, 'category.html', context)


def index1(request):
    return render(request, 'login.html')

def index2(request):
    return render(request, 'signup.html')

def create_user(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/reg_signup')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'], password= password)
        request.session['uid']= user.id
        return redirect('/')
    
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['uid'] = logged_user.id
            return redirect('/')
        else:
            messages.error(request, 'Email and password did not match')
            
    else:
        messages.error(request, 'Email is not registered')
    return redirect('/reg_login')


def create(request):
    if "uid" not in request.session:
        return redirect('/reg_login')
    if request.method == 'GET':
        categories = Categories.objects.all()
        context = {
            'categories' : categories
        }
        return render(request, 'add_business.html', context)
    elif request.method == 'POST':
        user = User.objects.filter(id = request.session['uid'])[0]
        name = request.POST['name']
        email = request.POST['email']
        street = request.POST['street']
        city = request.POST['city']
        phone_number = request.POST['phone_number']
        description = request.POST['description']
        work_from_hour = request.POST['work_from']
        work_to_hour = request.POST['work_to']
        break_from_hour = request.POST['break_from']
        break_to_hour = request.POST['break_to']
        longitude = request.POST['longitude']
        latitude = request.POST['latitude']
        business_days = request.POST.getlist('working_days')
        categories = request.POST.getlist('categories')
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(get_random_string(6) + '_' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        new_business = Business.objects.create(name=name,email=email,phone_number=phone_number,description=description, user=user, image_url = uploaded_file_url, longitude = longitude, latitude = latitude)
        business_hours = BusinessHours.objects.create(business = new_business, work_from_hour = work_from_hour, work_to_hour = work_to_hour, break_from_hour = break_from_hour, break_to_hour = break_to_hour)
        for bd in business_days:
            BusinessDays.objects.create(business = new_business, day = bd)
        for category in categories:
            Categories.objects.get(id = category).businesses.add(new_business)
        business_adress = BussinesAddress.objects.create(business = new_business, street = street, city = city)

    return redirect("/business/add")


def addreview(request, id):
    if request.method == 'POST':
        business = Business.objects.get(id=id)
        user = User.objects.filter(id = request.session['uid'])[0]
        review = BusinessReviews.objects.create(review = request.POST['review'], rating = request.POST['rating'], business = business, user = user)
    return redirect("/business/" + str(id))


def edit_business(request, id):
    if "uid" not in request.session:
        return redirect('/')
    if request.method == 'GET':
        try:
            business = Business.objects.get(id=id, user_id = request.session['uid'])
            if business:
                categories = Categories.objects.all()
                selected_categories_ids = business.categories.values_list('id', flat=True)
                selected_days_ids = business.business_days.values_list('day', flat=True)
                
                context = {
                    'categories' : categories,
                    'business' : business,
                    'selected_categories_ids' : selected_categories_ids,
                    'selected_days_ids' : selected_days_ids
                }
                return render(request, 'edit_business.html', context)
        except:
            return redirect("/")

    elif request.method == 'POST':
        try:
            business = Business.objects.get(id=id, user_id = request.session['uid'])
            if business:
                business.user = User.objects.filter(id = request.session['uid'])[0]
                business.name = request.POST['name']
                business.email = request.POST['email']
                business.phone_number = request.POST['phone_number']
                business.description = request.POST['description']

                business.address.street = request.POST['street']
                business.address.city = request.POST['city']
                business.address.save()
                business.business_hours.work_from_hour = request.POST['work_from']
                business.business_hours.work_to_hour = request.POST['work_to']
                business.business_hours.break_from_hour = request.POST['break_from']
                business.business_hours.break_to_hour = request.POST['break_to']
                business.business_hours.save()
            
                business.categories.clear()
                # business.business_hours.clear()
                business.business_days.all().delete()

                business_days = request.POST.getlist('working_days')
                categories = request.POST.getlist('categories')

                business.longitude = request.POST['longitude']
                business.latitude = request.POST['latitude']

                myfile = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(get_random_string(6) + '_' + myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                business.image_url = uploaded_file_url
                for bd in business_days:
                    BusinessDays.objects.create(business = business, day = bd)
                for category in categories:
                    Categories.objects.get(id = category).businesses.add(business)
                business.save()
        except:
            return redirect("/")
    return redirect("/")
       

def show_business(request, id):
    if request.method == 'GET':
        business = Business.objects.get(id=id)
        categories = business.categories.all()
        reviews = business.business_reviews.all()
        context = {
            'business' : business,
            'categories' : categories,
            'reviews' : reviews
        }
        return render(request, 'show_business.html', context)

def delete_business(request, id):
    business = Business.objects.get(id=id)
    business.delete()

    return redirect('/')

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def logout(request):
    if request.method == 'GET':
        del request.session['uid']
        return redirect('/')