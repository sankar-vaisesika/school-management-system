from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    USER_TYPE_CHOICES=(
        ('teacher','Teacher'),
        ('student','Student'),
    )

    user_type=models.CharField(max_length=10,choices=USER_TYPE_CHOICES,null=False,blank=False)


    def __str__(self):
        
        return f"{self.username} - {self.user_type}"
    
class Department(models.Model):

    name=models.CharField(max_length=100,unique=True)

    hod=models.OneToOneField('TeacherProfile',on_delete=models.SET_NULL,null=True,blank=True,related_name='headed_department')

    def __str__(self):

        return self.name

class TeacherProfile(models.Model):

    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)

    teacher_id=models.CharField(max_length=6,unique=True,blank=True)

    subject=models.CharField(max_length=100,null=False,blank=False)

    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True,related_name='teachers')


    def __str__(self):
        return f"{self.user.username} - {self.subject} - {self.teacher_id}"
    
    def save(self, *args, **kwargs):

        if not self.teacher_id:
        
            last = TeacherProfile.objects.order_by('-id').first()
        
            last_number = int(last.teacher_id[2:]) if last and last.teacher_id else 99
        
            self.teacher_id = f"TS{last_number + 1}"
        
        super().save(*args, **kwargs)


class StudentProfile(models.Model):

    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,primary_key=True)

    student_id=models.CharField(max_length=6,unique=True,blank=True)

    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name="students")

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
    
    def save(self, *args, **kwargs):
        
        if not self.student_id:
        
            last = StudentProfile.objects.order_by('-id').first()
        
            new_id = 100000 if not last else int(last.student_id) + 1
        
            self.student_id = str(new_id)
        
        super().save(*args, **kwargs)


