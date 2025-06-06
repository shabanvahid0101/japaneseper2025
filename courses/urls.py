
from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('upload/', views.upload_content, name='upload_content'),
    path('register/', views.register, name='register'),
    path('api/courses/', views.CourseListAPI.as_view(), name='course_list_api'),
    path('api/contents/', views.ContentListAPI.as_view(), name='content_list_api'),
    path('publish-report/', views.publish_report, name='publish_report'),
]