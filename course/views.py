from rest_framework import viewsets, status,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Department, Course,Review,Comment,Transaction,UserBankAccount,Enroll
from .serializers import DepartmentSerializer, CourseSerializer,ReviewSerializer,CommentSerializer,TransactionReportSerializer,DepositSerializer
from django.http import Http404 
from rest_framework.generics import CreateAPIView,ListAPIView
from django.db.models import Sum
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.utils import timezone
class DepartmentForInstructor(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        instructor_id = request.query_params.get("instructor_id")
        if instructor_id:
            return queryset.filter(course__instructor_id=instructor_id)
        return queryset
class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DepartmentForInstructor]
    
class CourseList(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['department__name', 'instructor__user__first_name','instructor__user__last_name','instructor__id']
    def get_queryset(self):
        queryset = super().get_queryset() 
        instructor_id = self.request.query_params.get('instructor_id')
        if instructor_id:
            queryset = queryset.filter(instructor_id=instructor_id)
        return queryset
    
class CourseDetail(APIView):
    

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        course = self.get_object(pk)
        if course.instructor != request.user.instructor:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def post(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ReviewViewset(viewsets.ModelViewSet):
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  
    serializer_class = CommentSerializer

class CourseComments(APIView):
    
    def get(self, request, course_pk, format=None):
        try:
            course = Course.objects.get(pk=course_pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(course=course)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, course_pk, format=None):
        try:
            course = Course.objects.get(pk=course_pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepositMoneyView(CreateAPIView):
    serializer_class = DepositSerializer


    def perform_create(self, serializer):
        amount = serializer.validated_data.get('amount')
        user_account, created = UserBankAccount.objects.get_or_create(user=self.request.user, defaults={'balance': 0})
        user_account.balance += amount
        user_account.save(update_fields=['balance'])

        transaction = Transaction.objects.create(
            account=user_account,
            amount=amount,
            balance_after_transaction=user_account.balance,
            transaction_type=1 
        )

      

        return transaction

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'detail': f'{serializer.validated_data.get("amount")}$ was deposited to your account successfully'}, status=status.HTTP_201_CREATED)

class TransactionReportView(ListAPIView):
    serializer_class = TransactionReportSerializer
    

    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account)

        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        balance = queryset.aggregate(Sum('amount'))['amount__sum'] if queryset else self.request.user.account.balance
        return Response({
            'transactions': serializer.data,
            'balance': balance
        })

class EnrollCourseView(APIView):
    def post(self, request, course_id, format=None):
        # Fetch the course or return 404 if not found
        course = get_object_or_404(Course, pk=course_id)

        # Check if the user has enough balance to enroll in the course
        account = request.user.account
        if account.balance < course.fee:
            return Response({'detail': 'Insufficient balance to enroll in the course.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the course fee from the user's balance
        account.balance -= course.fee
        account.save()

        # Create a new Enroll instance
        enroll = Enroll.objects.create(
            user=request.user,
            courses=course,
            enroll_date=timezone.now(),
            amount=course.fee
        )

        # Log the transaction
        transaction = Transaction.objects.create(
            account=account,
            amount=-course.fee,
            balance_after_transaction=account.balance,
            timestamp=enroll.enroll_date,
            transaction_type=1  # Assuming 1 is the type for enrollment
        )

        # Respond with success message
        return Response({'detail': f'You have successfully enrolled in {course.title}.'}, status=status.HTTP_201_CREATED)