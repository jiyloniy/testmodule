from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import include
from user.views2 import RegistetCompanyView,LoginView,RegistetTeacherView,RegistetStudentView,LogoutView, \
    RefreskTokenView 
from user.student import get_student, get_student_by_id, update_student,delete_student

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistetCompanyView.as_view(), name='register'),
    path('register_teacher/', RegistetTeacherView.as_view(), name='register_teacher'),
    path('students/', get_student, name='get_students'),
    path('studentcreate/', RegistetStudentView.as_view(), name='register_student'),
    path('studentget/<int:pk>/', get_student_by_id, name='get_student_by_id'),
    path('studentput/<int:pk>/', update_student, name='update_student'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreskTokenView.as_view(), name='refresh'), 
]
   
