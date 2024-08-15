from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('department', views.DepartmentViewset)
router.register('courses', views.CourseList)
router.register('reviews', views.ReviewViewset) 
router.register('comment', views.CommentViewset) 
router.register('balance', views.DepositView, basename="balance")

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course_detail'),
    path('courses/<int:course_pk>/comments/', views.CourseComments.as_view(), name='course-comments'),
    path('enroll/<int:id>/', views.EnrollmentView.as_view(), name='enroll'),
    path('enrollments/', views.UserEnrollmentsView.as_view(), name='user_enrollments'),
    path('balanceview/', views.DepositBalanceView.as_view(), name='user_balance'),
]
