from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('department', views.DepartmentViewset)
router.register('courses', views.CourseList)
router.register('reviews', views.ReviewViewset) 
router.register('comment', views.CommentViewset) 
# router.register(r'money-deposits', views.MoneyDepositView, basename='moneydeposit')




urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course_detail'),
    path('courses/<int:course_pk>/comments/', views.CourseComments.as_view(), name='course-comments'),
     path('course/enrollments/<int:student_id>/', views.StudentEnrollmentsView.as_view(), name='student-enrollments'),
    path('enrolls/<int:course_pk>/', views.EnrollmentView.as_view(), name='user_enrollments'),
    path('enrolls/<int:course_pk>/status/', views.EnrollmentStatusView.as_view(), name='enrollment_status'),
    path('enrollview/<int:pk>/', views.StudentEnrollmentsView.as_view(), name='user_view'),
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('balance/', views.DepositBalanceView.as_view(), name='deposit_balance'),
    path('deposit/payment/<str:trans_id>/<int:student_id>/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('deposit/pay/<int:student_id>/<int:check>/', views.PaymentUnSuccessView.as_view(), name='payment_unsuccess'),

]
