from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from django.contrib.auth import authenticate
from users.models import StudentProfile,TeacherProfile
from users.serializers import StudentProfileSerializer,TeacherProfileSerializer
# from users.permissions import IsAdmin,IsStudent,IsTeacher,IsTeacherorAdmin
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserRegistrationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            user=serializer_instance.save()

            user_type=serializer_instance.validated_data.get("user_type")

            if user_type == "student":

                StudentProfile.objects.create(user=user)

            elif user_type == "teacher":

                subject=request.data.get("subject")

                if not subject:

                    user.delete()

                    return Response({"error":"subject is required"})

                TeacherProfile.objects.create(user=user,subject=subject)

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
class LoginView(APIView):

    def post(self,request,*args,**kwargs):

        uname=request.data.get("username")

        pwd=request.data.get("password")

        user_instance=authenticate(username=uname,password=pwd)

        if user_instance:
        
            if user_instance.user_type=="teacher":

                students=StudentProfile.objects.all()
                
                student_serializer=StudentProfileSerializer(students,many=True)
                
                return Response(data=student_serializer.data)
        
        else:

            return Response(data={'message':"invalid credetials"})
        
class StudentListView(APIView):

    # permission_classes=[IsAuthenticated,IsTeacherorAdmin]

    def get(self,request,*args,**kwargs):

        student_instance=StudentProfile.objects.all()

        serializer_instance=StudentProfileSerializer(student_instance,many=True)

        return Response(data=serializer_instance.data)
        
class StudentProfileDetailUpdateDeleteView(APIView):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        student_instance=get_object_or_404(StudentProfile,id=id)

        serializer_instance=StudentProfileSerializer(student_instance)

        return Response(data=serializer_instance.data)
    
    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        student_instance=get_object_or_404(StudentProfile,id=id)

        serializer_instance=StudentProfileSerializer(data=request.data,instance=student_instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        
    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        student_instance=get_object_or_404(StudentProfile,id=id)
        
        user=student_instance.user

        user.delete()

        return Response(data={"message":"deleted successfully"})
    
class TeacherListView(APIView):

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


