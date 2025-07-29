from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from users.serializers import UserRegistrationSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from django.contrib.auth import authenticate
from users.models import StudentProfile,TeacherProfile,Department,CustomUser,Subject
from users.serializers import StudentProfileSerializer,TeacherProfileSerializer,SubjectSerializer
from users.permissions import IsAdmin,IsHOD,IsTeacherorAdmin
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        serializer_instance = UserRegistrationSerializer(data=request.data)

        if serializer_instance.is_valid():
            user=serializer_instance.save()

            return Response({"message": "User registered successfully!",
                              "user_id": user.id,
                              "username": user.username,
                              "user_type": user.user_type})
        
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

class TeacherListView(APIView):

    permission_classes=[IsAuthenticated,IsAdmin]

    def get(self,request,*args,**kwargs):

        qs=TeacherProfile.objects.all()

        serializer_instance=TeacherProfileSerializer(qs,many=True)

        return Response(data=serializer_instance.data)
        
class StudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_staff:
            # Admin - get all students
            students = StudentProfile.objects.all()

        elif user.user_type == 'teacher' and hasattr(user, 'teacherprofile'):
            teacher_profile = user.teacherprofile
            if teacher_profile.department.hod == teacher_profile:
                # HOD - get students of their department only
                students = StudentProfile.objects.select_related('user', 'department') \
                            .filter(department=teacher_profile.department)
            else:
                return Response({"detail": "Only HOD can view students."})
        else:
            return Response({"detail": "You do not have permission to view students."})

        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)
            
class SubjectCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            return Response(SubjectSerializer(subject).data)
        return Response(serializer.errors)

class SubjectListView(APIView):

    def get(self,request,*args,**kwargs):
        dept_id=kwargs.get("dept_id")

        department=get_object_or_404(Department,id=dept_id) 
        subjects=department.subjects.all()
        serializer_instance=SubjectSerializer(subjects,many=True)

        return Response(data=serializer_instance.data) 

class SubjectUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(instance=subject, data=request.data, partial=True)
        if serializer.is_valid():
            updated_subject = serializer.save()
            return Response(SubjectSerializer(updated_subject).data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()
        return Response({"message": "Subject deleted."})    

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
    
