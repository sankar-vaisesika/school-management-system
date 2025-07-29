from django.contrib import admin


# Register your models here.

from users.models import CustomUser,StudentProfile,TeacherProfile,Department

from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser,UserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(Department)
