from django.urls import path

from users import views

urlpatterns=[
    path('register/',views.UserRegistrationView.as_view(),name='user-register'),
    path('login/',views.LoginView.as_view()),
    path('student/<int:pk>/',views.StudentProfileUpdateDeleteView.as_view()),
    # path('student/<int:pk>/',views.StudentRetrieveView.as_view()),
    path('student/',views.StudentListView.as_view()),
    path('teacher/',views.TeacherListView.as_view()),
    path('teacher/<int:pk>/',views.TeacherProfileDetailUpdateDeleteView.as_view()),
    

]