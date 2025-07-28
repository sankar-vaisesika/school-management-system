from rest_framework import serializers
from users.models import CustomUser, StudentProfile, TeacherProfile,Department

class UserRegistrationSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'user_type', 'department_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if not data.get("department_name"):
            raise serializers.ValidationError("Department name is required")
        return data

    def create(self, validated_data):
        department_name = validated_data.pop('department_name')
        user_type = validated_data['user_type']

        # Get or create department
        department, _ = Department.objects.get_or_create(name=department_name)

        # Create user
        user = CustomUser.objects.create_user(**validated_data)

        # Create profile
        if user_type == 'teacher':
            TeacherProfile.objects.create(user=user, department=department)
        elif user_type == 'student':
            StudentProfile.objects.create(user=user, department=department)

        return user

    
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:

        model=Department

        fields=['id','name']

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


