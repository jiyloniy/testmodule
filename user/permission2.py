from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from typing import Any
from user.model2 import Student, Company, Teacher

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        
        print('request.user is teacher', request.user)
        return bool(
            request.user and
            request.user.is_authenticated and Teacher.objects.filter(user=request.user).exists()
        )
class IsTeacherOrCompany(BasePermission):
    def has_permission(self, request, view):
        print('request.user is teacher or company', request.user)
        return bool(
            request.user and
            request.user.is_authenticated and
            (Teacher.objects.filter(user=request.user).exists() or
             Company.objects.filter(user=request.user).exists())
        )
    
class IsStudent(BasePermission):
    def has_permission(self, request: Request, view: Any) -> bool:
        print('request.user is student', request.user),
        return bool(
            
            request.user and
            request.user.is_authenticated and Student.objects.filter(user=request.user).exists()
        )

class IsStudentOrCompanyOrTeacher(BasePermission):
    def has_permission(self, request, view):
        print('request.user is student or teacher or company', request.user)
        return bool(
            request.user and
            request.user.is_authenticated and
            (Student.objects.filter(user=request.user).exists() or
             Teacher.objects.filter(user=request.user).exists() or
             Company.objects.filter(user=request.user).exists())
        )
    
class IsCompany(BasePermission):
    def has_permission(self, request, view):

        print('request.user is company', request.user),
        return bool(
            
            request.user and
            request.user.is_authenticated and Company.objects.filter(user=request.user).exists()
        )
    
