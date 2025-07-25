from rest_framework import serializers
from users.models import CustomUser, StudentProfile, TeacherProfile,Department

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type','password']
        extra_kwargs={
            'password':{'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password properly
        user.save()
        return user
    
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:

        model=Department

        fields=['id','name']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department=DepartmentSerializer()

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'student_id','department']

class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department=DepartmentSerializer()

    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'teacher_id', 'subject','department']
class TeacherMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['teacher_id', 'subject']

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
