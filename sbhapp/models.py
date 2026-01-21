from django.db import models

# Create your models here.
class Enquiry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contactno = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    enqdate = models.DateTimeField(auto_now_add=True)

class LoginInfo(models.Model):
    usertype = models.CharField(max_length=20)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=256)
    status = models.CharField(max_length=10,default='active')
    def _str_(self):
        return f"{self.username}-{self.usertype}"

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    contactno = models.CharField(max_length=15)
    address = models.TextField()
    picture = models.ImageField(upload_to='profiles',blank=True)
    bio = models.TextField()
    login = models.OneToOneField(LoginInfo,on_delete=models.CASCADE)
    def _str_(self):
        return f"{self.name}-{self.email}"
    
