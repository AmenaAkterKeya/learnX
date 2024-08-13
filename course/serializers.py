from rest_framework import serializers
from .models import Department, Course,Review,Comment,Transaction,Enroll

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    # instructor = serializers.StringRelatedField(many=False)
    # department = serializers.StringRelatedField(many=True)
    
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
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_amount(self, value):
        min_deposit_amount = 100
        if value < min_deposit_amount:
            raise serializers.ValidationError(f'You need to deposit at least {min_deposit_amount} $')
        return value

class TransactionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'balance_after_transaction', 'timestamp', 'transaction_type']
        
class EnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = '__all__'