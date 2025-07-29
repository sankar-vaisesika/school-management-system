from django.urls import path

from users import views

urlpatterns=[
    path('register/',views.UserRegistrationView.as_view(),name='user-register'),
    path('login/',views.LoginView.as_view()),
    path('students/',views.StudentListView.as_view()),
    path('teachers/',views.TeacherListView.as_view()),
    path('subjects/create/',views.SubjectCreateView.as_view(),name='create-subject'),
    path('subjects/department/<int:dept_id>/', views.SubjectListView.as_view(), name='list-subjects'),
    path('subjects/<int:pk>/', views.SubjectUpdateDeleteView.as_view(), name='update-delete-subject'),


]