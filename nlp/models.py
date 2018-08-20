import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class SlackUser(models.Model):
    """
    Slack User models

    """
    
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def _str_(self):
      """
       str method
       Returns
      -----------
       str
         username
      """
      return self.username

    def authenticate(self,username,password):
        """
        authenticate method
        Parameters
        ----------
        username : str
         user name
        password : str
           password  
         Returns
         -----------
          bool
           true if authentication is successful and false if it fails.
         """

        check = None
        error_username = None
        error_password = None
        if self.username == username:

           if self.password == password:
              check = True
           else :
             error_password = "InValid Password"
             check = False  
        else :
             error_username = "InValid UserName"           
        return check,error_username,error_password
          
