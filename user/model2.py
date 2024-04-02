from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='companies/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['id']
        db_table = 'company'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Students'
        ordering = ['id']
        db_table = 'student'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    phone_2 = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='teachers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Teachers'
        ordering = ['id']
        db_table = 'teacher'


