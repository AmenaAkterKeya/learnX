from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)
    mobile_no = models.CharField(max_length = 12)
    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)
    mobile_no = models.CharField(max_length = 12)
    def __str__(self):
        return self.user.username
