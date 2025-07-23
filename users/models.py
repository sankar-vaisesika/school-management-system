from django.db import models
from random import randint
# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    USER_TYPE_CHOICES=(
        ('teacher','Teacher'),
        ('student','Student'),
    )

    user_type=models.CharField(max_length=10,choices=USER_TYPE_CHOICES,default='student')


    def __str__(self):
        
        return f"{self.username} - {self.user_type}"

class TeacherProfile(models.Model):

    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)

    teacher_id=models.CharField(max_length=6,unique=True,blank=True)

    subject=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.teacher_id}"


class StudentProfile(models.Model):

    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)

    student_id=models.CharField(max_length=6,unique=True,blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
