import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class SlackUser(models.Model):
    
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def _str_(self):
      return self.username

    def authenticate(self,username,password):

        check = None
        if self.username == username:

           if self.password == password:
              check = True
           else :

             check = False        
        return check
          
