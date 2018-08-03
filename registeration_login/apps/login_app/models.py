from django.db import models
import bcrypt


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

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateField(null = True)
    travel_date_to = models.DateField(null = True)
    created_by = models.ForeignKey(User, related_name="created_trips", null=True)
    user_on_trip = models.ManyToManyField(User, related_name="trips", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

