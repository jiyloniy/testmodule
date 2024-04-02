# perrmisions for user model
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from typing import Any
from user.models import User as UserModel


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        try:
            user_type = UserModel.objects.get(user=request.user).user_type
        except:
            return False

        return bool(
            request.user and
            request.user.is_authenticated and
            user_type == 'teacher'
        )


class IsStudent(BasePermission):
    def has_permission(self, request: Request, view: Any) -> bool:
        try:
            user_type = UserModel.objects.get(user=request.user).user_type
        except:
            return False

        return bool(
            request.user and
            request.user.is_authenticated and
            user_type == 'student'
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            user_type = UserModel.objects.get(user=request.user).user_type
        except:
            return False

        return bool(
            request.user and
            request.user.is_authenticated and
            user_type == 'admin'
        )
