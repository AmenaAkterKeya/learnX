from django.db import models
from rest_framework import serializers
from .models import Department, Course,Review,Comment,Balance,Enroll
class DepartmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Department
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    # instructor = serializers.StringRelatedField(many=False)
    # department = serializers.StringRelatedField(many=True)
    total_enrollments = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    total_courses_in_department = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor', 'created_on']
    def get_total_enrollments(self, obj):
        return Enroll.objects.filter(course=obj).count()
    def get_total_courses_in_department(self, obj):
        department_counts = {}
        for department in obj.department.all():
            course_count = Course.objects.filter(department=department).count()
            department_counts[department.name] = course_count
        return department_counts
    def get_total_amount(self, obj):
        total_fee = Enroll.objects.filter(course=obj).aggregate(total=models.Sum('course__fee'))['total']
        return total_fee or 0

    def get_students(self, obj):
        all_enrollments = Enroll.objects.filter(course=obj)
        recent_enrollments = all_enrollments.order_by('-enrolled_on')[:4]
        recent_student_data = []
        all_student_data = []
        
        for enrollment in recent_enrollments:
            recent_student_data.append({
                'username': enrollment.student.user.username,
                'email': enrollment.student.user.email,
                'enrolled_on': enrollment.enrolled_on,
            })
        
        for enrollment in all_enrollments:
            all_student_data.append({
                'username': enrollment.student.user.username,
                'email': enrollment.student.user.email,
                'enrolled_on': enrollment.enrolled_on,
            })
        
        return {
            'recent_students': recent_student_data,
            'all_students': all_student_data,
        }
    def create(self, validated_data):
        request = self.context.get('request')
        instructor = request.user.instructor  
        validated_data['instructor'] = instructor
        return super().create(validated_data)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer', 'instructor', 'created']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            student = request.user.student
            course = validated_data.get('course')
            if not Enroll.objects.filter(student=student, course=course).exists():
                raise serializers.ValidationError("You must be enrolled in the course to leave a review.")

            validated_data['reviewer'] = student
            validated_data['instructor'] = course.instructor

        return super().create(validated_data)
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
        read_only_fields = ['student', 'created_on']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['student'] = request.user.student
        return super().create(validated_data)

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = '__all__'
        read_only_fields = ['student', 'created_on']
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['student'] = request.user.student
        return super().create(validated_data)
  


