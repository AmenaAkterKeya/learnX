from rest_framework import viewsets, status,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Department, Course,Review,Comment,Balance,Enroll
from .serializers import DepartmentSerializer, CourseSerializer,ReviewSerializer,EnrollmentSerializer,CommentSerializer,DepositSerializer
from django.http import Http404
from sslcommerz_lib import SSLCOMMERZ
from django.http import HttpResponseRedirect
from rest_framework import status
from accounts.models import Student
from django.db.models import Sum
from django.views import View
from rest_framework.permissions import IsAuthenticated
import uuid
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

# class MoneyDepositView(viewsets.ModelViewSet):
#     serializer_class = DepositSerializer

#     def get_queryset(self):
#         return Balance.objects.filter(student=self.request.user.student)
class DepositView(APIView):
    def post(self, request, format=None):
        settings = {
            'store_id': 'learn671e7f86e7018',  
            'store_pass': 'learn671e7f86e7018@ssl',  
            'issandbox': True  
        }

        sslcz = SSLCOMMERZ(settings)

        deposit_amount = request.data.get('amount', None)

        # Validate deposit amount
        if deposit_amount is None or float(deposit_amount) < 200:
            return Response({'error': 'Please enter an amount of at least 200 BDT.'}, status=status.HTTP_400_BAD_REQUEST)  # Error handling for insufficient amount

        try:
            student = Student.objects.get(user=request.user)  # Fetching student details
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)  # Error if student not found

        transaction_id = str(uuid.uuid4())  # Generating a unique transaction ID

        post_body = {
            'total_amount': deposit_amount,
            'currency': "BDT",
            'tran_id': transaction_id,  
            'success_url': f'https://learn-x-seven.vercel.app/course/deposit/payment/{transaction_id}/{student.id}/',
            'fail_url': f'https://learn-x-seven.vercel.app/course/deposit/pay/{student.id}/0/',
            'cancel_url': f'https://learn-x-seven.vercel.app/course/deposit/pay/{student.id}/0/',
            'emi_option': 0,
            'cus_name': student.user.first_name,
            'cus_email': student.user.email,
            'cus_phone': "01700000",  
            'cus_add1': "Uttara",
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': "Deposit",
            'product_category': "Deposit",
            'product_profile': "general"
        }

        try:
            response = sslcz.createSession(post_body)
            # print(response)
            return Response({'url': response['GatewayPageURL']}, status=status.HTTP_200_OK)  
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
class PaymentSuccessView(APIView):
    def post(self, request, trans_id, student_id):
    
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

        amount = request.data.get('amount')
        if amount is None:
            return Response({'error': 'Amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

        Balance.objects.create(student=student, amount=amount)

        return  HttpResponseRedirect('https://amenaakterkeya.github.io/learnX_frontend/enroll_course.html')
class PaymentUnSuccessView(APIView):
    def post(self, request,student_id,check ):
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

        if check == 0:
           return HttpResponseRedirect('https://amenaakterkeya.github.io/learnX_frontend/de.html')
            

        return HttpResponseRedirect('https://amenaakterkeya.github.io/learnX_frontend/de.html')

class DepositBalanceView(APIView):
    def get(self, request, format=None):
        student = request.user.student
        deposits = Balance.objects.filter(student=student)
        deposit_serializer = DepositSerializer(deposits, many=True)
        initial_balance = sum(deposit.amount for deposit in deposits)
        total_deposit = deposits.aggregate(total=Sum('amount'))['total'] or 0.00

        return Response({
            "updated_balance": initial_balance, 
            "deposits": deposit_serializer.data,
            "total_deposit": total_deposit
        }, status=status.HTTP_200_OK)
class EnrollmentView(APIView):
    def post(self, request, course_pk, format=None):
        course = Course.objects.get(pk=course_pk)
        student = request.user.student
        if Enroll.objects.filter(student=student, course=course).exists():
            return Response({
                "error": "You are already enrolled in this course"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        deposits = Balance.objects.filter(student=student)
        total_balance = sum(deposit.amount for deposit in deposits)
        if total_balance < course.fee:
            return Response({
                "error": "Insufficient balance",
                "current_balance": total_balance
            }, status=status.HTTP_400_BAD_REQUEST)
        Enroll.objects.create(student=student, course=course)
        remaining_balance = total_balance - course.fee
        Balance.objects.create(student=student, amount=-course.fee)

        return Response({
            "message": "Enrollment successful",
            "current_balance": remaining_balance
        }, status=status.HTTP_201_CREATED)
class EnrollmentStatusView(APIView):
    def get(self, request, course_pk, format=None):
        student = request.user.student
        enrolled = Enroll.objects.filter(student=student, course_id=course_pk).exists()
        return Response({'enrolled': enrolled}, status=status.HTTP_200_OK)
class StudentEnrollmentsView(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)

        # Get enrollments for the student
        enrollments = Enroll.objects.filter(student=student).select_related('course', 'course__instructor')

        enrolled_courses = [
            {
                "course_id": enrollment.course.id,
                "course_title": enrollment.course.title,
                "course_fee": enrollment.course.fee,
                "course_lesson": enrollment.course.lesson,
                "instructor": enrollment.course.instructor.user.first_name,
            }
            for enrollment in enrollments
        ]

        total_courses_purchased = enrollments.count()

        total_deposit = Balance.objects.filter(student=student).aggregate(total=Sum('amount'))['total'] or 0.00
        total_purchase = sum(enrollment.course.fee for enrollment in enrollments)

        response_data = {
            "enrolled_courses": enrolled_courses,
            "total_deposit_amount": total_deposit,
            "total_purchase_amount": total_purchase,
            "total_courses_purchased": total_courses_purchased,
        }

        return Response(response_data, status=status.HTTP_200_OK)
