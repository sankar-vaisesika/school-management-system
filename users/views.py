from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from django.contrib.auth import authenticate
from users.models import StudentProfile
from users.serializers import StudentProfileSerializer,TeacherProfileSerializer
# Create your views here.

class UserRegistrationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
class LoginView(APIView):

    def post(self,request,*args,**kwargs):

        uname=request.data.get("username")

        pwd=request.data.get("password")

        user_instance=authenticate(username=uname,password=pwd)

        if user_instance:

            return Response(data={'message':"valid credentials"})
        
        else:

            return Response(data={'message':"invalid credetials"})
        
class StudentProfileDetailView(APIView):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        student_instance=get_object_or_404(StudentProfile,id=id)

        serializer_instance=StudentProfileSerializer(student_instance)

        return Response(data=serializer_instance.data)