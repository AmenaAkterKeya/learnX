from rest_framework import serializers
from .models import Department, Course,Review

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(many=False)
    department = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor', 'created_on']
    def create(self, validated_data):
        request = self.context.get('request')
        instructor = request.user.instructor  
        validated_data['instructor'] = instructor
        return super().create(validated_data)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'