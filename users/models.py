from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    USER_TYPE_CHOICES=(
        ('teacher','Teacher'),
        ('student','Student'),
    )

    user_type=models.CharField(max_length=10,choices=USER_TYPE_CHOICES)

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        
        return f"{self.username} - {self.user_type}"
    
class Department(models.Model):

    name=models.CharField(max_length=100,unique=True)

    hod=models.OneToOneField('TeacherProfile',on_delete=models.SET_NULL,null=True,blank=True,related_name='hod_department')

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.name
    
class TeacherProfile(models.Model):

    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,limit_choices_to={'user_type':'teacher'})

    teacher_id=models.CharField(max_length=6,unique=True,blank=True)

    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='teachers')

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -{self.department.name} - {self.teacher_id}"
    
    def save(self, *args, **kwargs):
        if not self.teacher_id:
            last_teacher = (
                TeacherProfile.objects
                .filter(teacher_id__regex=r'^TS\d+$')  # only valid teacher_ids
                .order_by('-id')
                .first()
            )
            if last_teacher and last_teacher.teacher_id:
                try:
                    last_id_num = int(last_teacher.teacher_id[2:])
                except ValueError:
                    last_id_num = 99  # fallback
            else:
                last_id_num = 99  # Start from TS100

            self.teacher_id = f"TS{last_id_num + 1}"
        super().save(*args, **kwargs)


class StudentProfile(models.Model):

    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,limit_choices_to={'user_type':'student'})

    student_id=models.CharField(max_length=6,unique=True,blank=True)

    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name="students")

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.department.name}- {self.student_id}"
    
    def save(self, *args, **kwargs):
        
        if not self.student_id:
        
            last = StudentProfile.objects.order_by('-id').first()
        
            new_id = 100000 if not last else int(last.student_id) + 1
        
            self.student_id = str(new_id)
        
        super().save(*args, **kwargs)

class Subject(models.Model):

    name=models.CharField(max_length=100)

    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='subjects')

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"{self.name}-{self.department.name}"
    
class Mark(models.Model):

    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name='marks')

    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='marks')

    mark_obtained=models.PositiveBigIntegerField()

    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together=('student','subject')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.mark_obtained}"


