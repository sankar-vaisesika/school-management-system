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
    username = serializers.CharField(source='user.username', required=False)
    department_name = serializers.CharField(write_only=True)
    department = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'username', 'department', 'department_name']

    def update(self, instance, validated_data):
        # Handle username update
        user_data = validated_data.pop('user', {})
        username = user_data.get('username')
        if username:
            instance.user.username = username
            instance.user.save()

        # Handle department update
        dept_name = validated_data.pop('department_name', None)
        if dept_name:
            try:
                department = Department.objects.get(name=dept_name)
                instance.department = department
            except Department.DoesNotExist:
                raise serializers.ValidationError({"department_name": "No department found with this name."})

        # Update other StudentProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TeacherProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    is_hod = serializers.BooleanField(required=False)
    department_name = serializers.CharField(write_only=True)
    department = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ['teacher_id', 'username', 'is_hod', 'department', 'department_name']

    def update(self, instance, validated_data):
    # Get username from nested user dict
        user_data = validated_data.pop('user', {})
        username = user_data.get('username')
        if username:
            instance.user.username = username
            instance.user.save()

        # Handle department update
        dept_name = validated_data.pop('department_name', None)
        if dept_name:
            try:
                department = Department.objects.get(name=dept_name)
                instance.department = department
            except Department.DoesNotExist:
                raise serializers.ValidationError({"department_name": "No department found with this name."})

        # Update TeacherProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance




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

    teacher_name=serializers.CharField(source='teacher.user.username',read_only=True)

    class Meta:
    
        model = Subject
    
        fields = ['id', 'name', 'department', 'department_name','teacher','teacher_name']

    def create(self, validated_data):
    
        dept_name = validated_data.pop('department_name')

        teacher = validated_data.get('teacher')

    
        try:
            department = Department.objects.get(name=dept_name)
        except Department.DoesNotExist:
            raise serializers.ValidationError({"department_name": "Department does not exist."})

        # 🔐 Validate that the teacher belongs to this department
        if teacher.department != department:
            raise serializers.ValidationError("Teacher does not belong to the given department.")

        # Create subject
        subject = Subject.objects.create(department=department, **validated_data)
        return subject

class MarkSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    teacher = TeacherProfileSerializer(read_only=True)

    class Meta:
        model = Mark
        fields = "__all__"
        
    def validate_mark_obtained(self,value):

        if value < 0 or value > 100:

            raise serializers.ValidationError("Mark must be between 0 to 100")
        
        return value