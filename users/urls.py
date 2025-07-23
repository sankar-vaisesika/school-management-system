from django.urls import path

from users import views

urlpatterns=[
    path('register/',views.UserRegistrationView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('student/<int:pk>/',views.StudentProfileDetailView.as_view()),
    
]