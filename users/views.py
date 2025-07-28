from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from users.serializers import UserRegistrationSerializer
from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from django.contrib.auth import authenticate
from users.models import StudentProfile,TeacherProfile,Department,CustomUser
from users.serializers import StudentProfileSerializer,TeacherProfileSerializer
from users.permissions import IsAdmin,IsTeacher,IsTeacherorAdmin
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        serializer_instance = UserRegistrationSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save()

            return Response({"message": "User registered successfully!"})
        
        return Response(serializer_instance.errors)

class LoginView(APIView):

    def post(self,request,*args,**kwargs):

        uname=request.data.get("username")

        pwd=request.data.get("password")

        if not uname or not pwd:
            return Response({"error": "Username and password are required"})

        user_instance=authenticate(username=uname,password=pwd)

        if user_instance:
        
            if user_instance.user_type=="teacher":

                students = StudentProfile.objects.all()
                student_serializer = StudentProfileSerializer(students, many=True)
                return Response({
                    "message": "Teacher logged in successfully",
                    "students": student_serializer.data
                })
            
            elif user_instance.user_type=="student":

                return Response(data={"message":"student logged in successfully"})
        
            else:

                return Response(data={'message':"invalid user type"})
            
        return Response({"error": "Invalid credentials"})
        
class StudentListView(ListAPIView):

        queryset=StudentProfile.objects.all()

        serializer_class=StudentProfileSerializer

        permission_classes=[IsAuthenticated,IsTeacherorAdmin]
    
class StudentRetrieveView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherorAdmin]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        student = get_object_or_404(StudentProfile, pk=pk)
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data)
        
class StudentProfileUpdateDeleteView(APIView):

    permission_classes=[IsAuthenticated,IsAdmin]

    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        student_instance=get_object_or_404(StudentProfile,user_id=id)

        serializer_instance=StudentProfileSerializer(data=request.data,instance=student_instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        student_instance=get_object_or_404(StudentProfile,user_id=id)
        
        user=student_instance.user

        user.delete()

        return Response(data={"message":"deleted successfully"})
    
class TeacherListView(APIView):

    permission_classes=[IsAuthenticated,IsAdmin]

    def get(self,request,*args,**kwargs):

        qs=TeacherProfile.objects.all()

        serializer_instance=TeacherProfileSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
    
class TeacherProfileDetailUpdateDeleteView(APIView):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        teacher_instance=get_object_or_404(TeacherProfile,id=id)

        serializer_instance=TeacherProfileSerializer(teacher_instance)

        return Response(data=serializer_instance.data)
    
    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        teacher_instance=get_object_or_404(TeacherProfile,id=id)

        serializer_instance=TeacherProfileSerializer(instance=teacher_instance,data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        teacher_instance=get_object_or_404(TeacherProfile,id=id)

        user=teacher_instance.user

        user.delete()

        return Response(data={"message":"deleted successfully"})