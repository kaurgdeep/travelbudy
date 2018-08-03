from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request,'login_app/index.html')

def processreg(request):
    result = User.objects.validate_registration(request.POST)
    if result['status']:    #that means if its true
        request.session['user_id'] = result['user_id']
        return redirect('/success')
    else:
        for error in result['errors']:
            messages.error(request,error)   
    return redirect('/')


def processlog(request):
    result = User.objects.validate_login(request.POST)
    if result['status']: #that means if its true
        request.session['user_id'] = result['user_id']
        return redirect('/success')
    else:
        for error in result['errors']:
            messages.error(request,error)    
    return redirect('/')


def success(request):
    # GET ALL TRIPS me = User.objects.get(id=request.session[‘user_id’])
    #context = {   #to send queries to HTML
       #‘my_trips’: Trip.objects.filter(joined_by=me),
       #‘not_my_trips’: Trip.objects.exclude(joined_by=me),
   #}
    context = {
        
        "all_trips": Trip.objects.all(),
        "my_trips": User.objects.get(id=request.session['user_id']).created_trips.all(),
        "others_trip":Trip.objects.exclude(created_by= User.objects.get(id=request.session['user_id']))#.exclude(user_on_trip=User.objects.get(id=request.session['user_id'])) 

    }
    # SHOW ON PAGE
    return render(request, 'login_app/success.html',context)

def logout(request):
    request.session.clear() 
    return redirect('/')

def add_travel_plan(request):

    return render(request, 'login_app/add.html')

def add(request):
    post_destination = request.POST['destination']
    post_description = request.POST['description']
    post_travel_date_from = request.POST['travel_date_from']
    post_travel_date_to = request.POST['travel_date_to']
    post_created_by = User.objects.get(id=request.session['user_id'])


    trip = Trip.objects.create(
        destination = post_destination,
        description = post_description,
        travel_date_from = post_travel_date_from,
        travel_date_to = post_travel_date_to,
        created_by = post_created_by 
        )
           
    #request.post to GET the data from the form
    print(trip.destination)
    # model.Create() to create new object in DB

    return redirect('/success')


def home(request):
    return redirect('/success')

def destination(request, trip_id):

    trip = Trip.objects.get(id=trip_id)
    
    context = {

        "current_trip": trip #or without variable "current_trip": Trip.objects.get(id=trip_id)
    }
    print(trip_id)
    return render(request,'login_app/destination.html', context)

def join(request):
    return render(request, 'login_app/destination.html')


    
   
   
#def destination(request): #get error if not add trip_id
    #print(trip_id)
    #return render(request, 'login_app/destination.html')
