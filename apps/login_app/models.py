from django.db import models
import bcrypt,datetime


class UserManager(models.Manager):
    def validate_registration(self, postData):
        response = {
           'status' : False,
           'errors' : []
        }
        if len(postData['first_name']) < 2:
           response['errors'].append("first_name too short")

        if len(postData['last_name']) < 2:
           response['errors'].append("last_name too short")

        if len(postData['email']) < 10:
           response['errors'].append("invalid email")

        if len(postData['password']) < 8:
            response['errors'].append("invalid password")

        if postData['confirm_pw'] != postData['password']:
            response['errors'].append("invalid password")
            

        if len(response['errors']) == 0:
            response['status'] = True
            response['user_id'] = User.objects.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            ).id
        return response 

    def validate_login(self, postData):
        response = {
           'status' : False,
           'errors' : []
        }
        #if len(User.objects.filter(eamil=postData['email'])) == 0:
        existing_users = User.objects.filter(email=postData['email'])
        if len(existing_users) == 0:
            print('errors')
            response['errors'].append("invalid input")
        else:
            if bcrypt.checkpw(postData['password'].encode(), existing_users[0].password.encode()):
                response['status'] = True
                response['user_id'] = existing_users[0].id
            else:
                print("invalid input")
        return response    
          

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class TripManager(models.Manager):

    def add(self, postData, user_id):
        response = {
           'status' : False,
           'errors' : []
        }
        print (postData)
        if len(postData['destination']) < 2:
           response['errors'].append("destination not valid")

        if len(postData['description']) < 2:
           response['errors'].append("description not valid")
        if len(postData['travel_date_from']) > 0:
            today = datetime.datetime.today()
            travel_date_from = datetime.datetime.strptime(postData['travel_date_from'], '%Y-%m-%d')
            if travel_date_from < today:
                response['errors'].append('Date cannot be in the past')
        if len(postData['travel_date_from']) < 1:
            response['errors'].append('Date required')
        

        # if len(postData['email']) < 10:
        #    response['errors'].append("invalid email")

        # if len(postData['password']) < 8:
        #     response['errors'].append("invalid password")

        # if postData['confirm_pw'] != postData['password']:
        #     response['errors'].append("invalid password")
            

        if len(response['errors']) == 0:
            response['status'] = True
            post_destination = postData['destination']#from here i'm saving POST info that I can create and save info in models
            post_description = postData['description']
            post_travel_date_from = postData['travel_date_from']
            post_travel_date_to = postData['travel_date_to']
            post_created_by = User.objects.get(id=user_id)


            trip = Trip.objects.create(
                destination = post_destination,
                description = post_description,
                travel_date_from = post_travel_date_from,
                travel_date_to = post_travel_date_to,
                created_by = post_created_by 
                )
            # trip.user_on_trip.add(post_created_by)
            # trip.save()
        
           
        return response 
    def join(self, trip_id, user_id):
        me = User.objects.get(id=user_id)
        trip = Trip.objects.get(id=trip_id)
        trip.user_on_trip.add(me)
        trip.save()


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateField(null = True)
    travel_date_to = models.DateField(null = True)
    created_by = models.ForeignKey(User, related_name="created_trips", null=True)
    user_on_trip = models.ManyToManyField(User, related_name="trips", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

