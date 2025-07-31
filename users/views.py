from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from users.serializers import UserRegistrationSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from django.contrib.auth import authenticate
from users.models import StudentProfile,TeacherProfile,Department,CustomUser,Subject,Mark
from users.serializers import StudentProfileSerializer,TeacherProfileSerializer,SubjectSerializer,MarkSerializer
from users.permissions import IsAdmin,IsAdminOrHOD,IsTeacherorAdmin
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

    permission_classes=[IsAuthenticated,IsAdmin]

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

    
class MarkCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        teacher_profile = get_object_or_404(TeacherProfile, user=request.user)

        serializer = MarkSerializer(data=request.data)

        if serializer.is_valid():
            student = serializer.validated_data['student']
            subject = serializer.validated_data['subject']

            if subject.teacher != teacher_profile:
                return Response({'detail': 'You are not the assigned teacher for this subject.'})

            if student.department != teacher_profile.department:
                return Response({'detail': 'Student does not belong to your department.'})

            serializer.save(teacher=teacher_profile)
            return Response(serializer.data)

        return Response(serializer.errors)

    
class MarkUpdateDeleteView(APIView):
    # permission_classes = [IsAuthenticated]

    # def delete(self, request, pk, *args, **kwargs):

    #     teacher_profile = get_object_or_404(TeacherProfile, user=request.user)
        
    #     mark_instance = get_object_or_404(Mark, pk=pk)

    #     # Check if the logged-in teacher is the subject teacher
    #     if mark_instance.subject.teacher != teacher_profile:
            
    #         return Response({"detail": "You are not allowed to delete this mark. Only the subject teacher can delete it."}, status=403)

    #     mark_instance.delete()
    #     return Response({"detail": "Mark deleted successfully."})

    permission_classes=[IsAuthenticated]

    def get_teacher_profile(self,request):

        return get_object_or_404(TeacherProfile,user=request.user)
    
    def get_mark_instance(self, pk, teacher_profile):
        mark = get_object_or_404(Mark, pk=pk)

        # Check permission: only the teacher who teaches the subject can modify
        if mark.subject.teacher != teacher_profile:
            return None, Response({'detail': 'Permission denied. You are not the subject teacher.'}, status=403)

        return mark, None

    def put(self, request, pk, *args, **kwargs):
        teacher_profile = self.get_teacher_profile(request)
        mark_instance, error = self.get_mark_instance(pk, teacher_profile)
        if error:
            return error

        serializer = MarkSerializer(instance=mark_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(teacher=teacher_profile)  # Optional, keeps consistency
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        teacher_profile = self.get_teacher_profile(request)
        mark_instance, error = self.get_mark_instance(pk, teacher_profile)
        if error:
            return error

        mark_instance.delete()
        return Response({'detail': 'Mark deleted successfully'}) 
    
class StudentMarkListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student_profile = request.user.studentprofile
        except:
            return Response({"detail": "You are not a student."})

        marks = Mark.objects.filter(student=student_profile)
        serializer = MarkSerializer(marks, many=True)
        return Response(serializer.data)
    
class HODStudentMarksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            teacher_profile = request.user.teacherprofile
        except:
            return Response({"detail": "You are not a teacher."})

        # Check if user is HOD
        if teacher_profile != teacher_profile.department.hod:
            return Response({"detail": "You are not the HOD."}, status=403)

        # Get all students in department
        department_students = StudentProfile.objects.filter(department=teacher_profile.department)

        # Get all marks for those students
        marks = Mark.objects.filter(student__in=department_students)
        serializer = MarkSerializer(marks, many=True)
        return Response(serializer.data)

class StudentReportView(APIView):

    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):

        student=get_object_or_404(StudentProfile,user=request.user)
        marks=Mark.objects.filter(student=student)

        total_marks=sum(mark.mark_obtained for mark in marks)
        total_subject=marks.count()
        average=round(total_marks/total_subject,2) if total_subject else 0

        mark_data = MarkSerializer(marks, many=True).data

        return Response({
            "student":student.user.username,
            "department":student.department.name,
            "total_marks":total_marks,
            "average":average,
            "subject_wise_marks":mark_data
        })


class SubjectTopperView(APIView):

    permission_classes=[IsAuthenticated,IsTeacherorAdmin]

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        subject=get_object_or_404(Subject, id=id)

        top_mark=Mark.objects.filter(subject=subject).order_by("-mark_obtained").first()

        if not top_mark:
            return Response({"detail": "No marks available for this subject."})

        return Response({
            "subject": subject.name,
            "topper": top_mark.student.user.username,
            "mark": top_mark.mark_obtained,
            "status": "Pass" if top_mark.mark_obtained >= 40 else "Fail"
        })


class DepartmentStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = get_object_or_404(TeacherProfile, user=request.user)
        department = getattr(teacher, 'hod_department', None)

        if department is None:
            return Response({"detail": "You are not HOD of any department."}, status=403)

        subjects = Subject.objects.filter(department=department)
        stats = []

        for subject in subjects:
            marks_qs = Mark.objects.filter(subject=subject)
            count = marks_qs.count()

            if count == 0:
                stats.append({
                    "subject": subject.name,
                    "average_mark": None,
                    "pass_percentage": None
                })
                continue

            total = sum(mark.mark_obtained for mark in marks_qs)
            average = round(total / count, 2)
            passed = marks_qs.filter(mark_obtained__gte=40).count()
            pass_percentage = round((passed / count) * 100, 2)

            stats.append({
                "subject": subject.name,
                "average_mark": average,
                "pass_percentage": pass_percentage
            })

        return Response({
            "department": department.name,
            "subjects_statistics": stats
        })
