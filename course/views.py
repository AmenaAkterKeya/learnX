from rest_framework import viewsets, status,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Department, Course,Review,Comment,Balance,Enroll
from .serializers import DepartmentSerializer, CourseSerializer,ReviewSerializer,EnrollmentSerializer,CommentSerializer,DepositSerializer
from django.http import Http404 
from django.shortcuts import get_object_or_404

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

class DepositView(viewsets.ModelViewSet):
    serializer_class = DepositSerializer

    def get_queryset(self):
        return Balance.objects.filter(student=self.request.user.student)

class EnrollmentView(APIView):
    def post(self, request, id, format=None):
        course = get_object_or_404(Course, id=id)
        student = request.user.student

        deposits = Balance.objects.filter(student=student)
        total_balance = sum(deposit.amount for deposit in deposits)
        if total_balance < course.fee:
            return Response({
                "error": "Insufficient balance",
                "current_balance": total_balance
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create enrollment
        Enroll.objects.create(student=student, course=course)

        # Deduct course fee from the balance
        remaining_balance = total_balance - course.fee
        Balance.objects.create(student=student, amount=-course.fee)

        return Response({
            "message": "Enrollment successful",
            "current_balance": remaining_balance
        }, status=status.HTTP_201_CREATED)

class UserEnrollmentsView(APIView):
    def get(self, request, format=None):
        student = request.user.student
        enrollments = Enroll.objects.filter(student=student)
        serializer = EnrollmentSerializer(enrollments, many=True)
        
        deposits = Balance.objects.filter(student=student)
        total_balance = sum(deposit.amount for deposit in deposits)
        course_fees = sum(enrollment.course.fee for enrollment in enrollments)
        current_balance = total_balance - course_fees

        return Response({
            "current_balance": current_balance,
            "enrollments": serializer.data
        }, status=status.HTTP_200_OK)

# class DepositBalanceView(APIView):
#     def get(self, request, format=None):
#         user = request.user
#         deposits = Balance.objects.filter(user=user)
#         deposit_serializer = DepositSerializer(deposits, many=True)

#         initial_balance = sum(deposit.amount for deposit in deposits)

#         enrollments = Enroll.objects.filter(user=user)
#         updated_balance = initial_balance
#         for enrollment in enrollments:
#             course_fee = enrollment.course.fee
#             updated_balance -= course_fee

#         return Response({
#             "initial_balance": initial_balance,
#             "updated_balance": updated_balance,
#             "deposits": deposit_serializer.data
#         }, status=status.HTTP_200_OK)

class DepositBalanceView(APIView):
    def get(self, request, format=None):
        student = request.user.student
        deposits = Balance.objects.filter(student=student)
        total_balance = sum(deposit.amount for deposit in deposits)
        
        return Response({
            "total_balance": total_balance
        }, status=status.HTTP_200_OK)