from django.db import models
from accounts.models import Instructor,Student

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
    image = models.ImageField(upload_to="course/course_pic/" ,null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.instructor.user.username}'

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