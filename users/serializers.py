from rest_framework import serializers
from users.models import CustomUser, StudentProfile, TeacherProfile,Department,Subject,Mark

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']

class UserRegistrationSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(write_only=True)
    is_hod = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'user_type', 'department_name','is_hod']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if not data.get("department_name"):
            raise serializers.ValidationError("Department name is required")
        return data

    def create(self, validated_data):
        department_name = validated_data.pop('department_name')
        user_type = validated_data['user_type']
        is_hod = validated_data.pop('is_hod', False)

        # Get or create department
        department, _ = Department.objects.get_or_create(name=department_name)

        # Create user
        user = CustomUser.objects.create_user(**validated_data)

        # Create profile
        if user_type == 'student':
            StudentProfile.objects.create(user=user, department=department)

        elif user_type == 'teacher':
            teacher_profile = TeacherProfile.objects.create(user=user, department=department)

            if is_hod and department.hod is None:
                department.hod = teacher_profile
                department.save()
        return user

    
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:

        model=Department

        fields=['id','name','hod']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(read_only=True)
    department=DepartmentSerializer()

    class Meta:
        model = StudentProfile
        fields = [ 'user', 'student_id','department']

class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(read_only=True)
    department=DepartmentSerializer()

    class Meta:
        model = TeacherProfile
        fields = [ 'user', 'teacher_id','department']
class TeacherMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['teacher_id']

class StudentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['student_id']

class DepartmentDetailSerializer(serializers.ModelSerializer):
    hod = TeacherMiniSerializer()
    teachers = TeacherMiniSerializer(many=True)
    students = StudentMiniSerializer(many=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'hod', 'teachers', 'students']


class SubjectSerializer(serializers.ModelSerializer):

    department_name = serializers.CharField(write_only=True)
    
    department = serializers.StringRelatedField(read_only=True)

    class Meta:
    
        model = Subject
    
        fields = ['id', 'name', 'department', 'department_name']

    def create(self, validated_data):
    
        dept_name = validated_data.pop('department_name')
    
        department, created = Department.objects.get_or_create(name=dept_name)
    
        subject = Subject.objects.create(department=department, **validated_data)
    
        return subject

class MarkSerializer(serializers.ModelSerializer):

    class Meta:

        model=Mark

        fields=['id','student','subject','mark_obtained','created_at']