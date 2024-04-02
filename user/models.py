from django.db import models
from django.contrib.auth.models import User as AuthUser


# Create your models here.

class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_choice = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_type = models.CharField(max_length=20, choices=user_choice, default='student')

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']


class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'leads_user'
        verbose_name = 'User lead'
        verbose_name_plural = 'Users leads'
        ordering = ['id']
