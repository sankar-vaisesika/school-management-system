from django.urls import path

from users import views

urlpatterns=[
    path('register/',views.UserRegistrationView.as_view(),name='user-register'),
    path('login/',views.LoginView.as_view()),
    path('students/',views.StudentListView.as_view()),
    path('teachers/',views.TeacherListView.as_view()),
    path('teachers/<int:pk>/',views.TeacherProfileDetailUpdateDeleteView.as_view()),
    path('students/<int:pk>/',views.StudentProfileUpdateDeleteView.as_view()),
    path('subjects/create/',views.SubjectCreateView.as_view(),name='create-subject'),
    path('subjects/department/<int:dept_id>/', views.SubjectListView.as_view(), name='list-subjects'),
    path('subjects/<int:pk>/', views.SubjectUpdateDeleteView.as_view(), name='update-delete-subject'),
    path('marks/',views.MarkCreateView.as_view(),name='marks'),
    path('marks/<int:pk>/',views.MarkUpdateDeleteView.as_view()),
    path('student/marks/', views.StudentMarkListView.as_view(), name='student-marks'),
    path('hod/department-marks/', views.HODStudentMarksView.as_view(), name='hod-marks'),

]