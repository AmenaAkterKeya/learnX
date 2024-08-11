from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('department', views.DepartmentViewset)
router.register('courses', views.CourseList)
router.register('reviews', views.ReviewViewset) 
router.register('comment', views.CommentViewset) 
urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course_detail'),
     path('courses/<int:course_pk>/comments/', views.CourseComments.as_view(), name='course-comments'),
]
