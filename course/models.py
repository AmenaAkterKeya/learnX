from django.db import models
from accounts.models import Instructor,Student
from django.contrib.auth.models import User
from .constants import TRANSACTION_TYPE
from django.utils import timezone
class Department(models.Model):
    name = models.CharField(max_length = 30)
    slug = models.SlugField(max_length = 40)
    def __str__(self):
        return self.name
    

class Course(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    content = models.TextField()
    department = models.ManyToManyField(Department) 
    lesson = models.IntegerField()
    fee = models.IntegerField()
    image = models.URLField(max_length=300 ,null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.instructor.user.username}'
class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Comments by {self.name}"

STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]
class Review(models.Model):
    reviewer = models.ForeignKey(Student, on_delete = models.CASCADE)
    instructor= models.ForeignKey(Instructor, on_delete = models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    
    def __str__(self):
        return f"Reviewer : {self.reviewer.user.first_name} ; Instructor : {self.instructor.user.first_name}"

class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Account"

 
class Transaction(models.Model):
    account = models.ForeignKey(UserBankAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Transaction by {self.account.user.username} on {self.timestamp}"   
    
class Enroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    enroll_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)  

    def __str__(self):
        return f'{self.user.username} enrolled in {self.courses.title}'
