from django.db import models
from user.models import User as UserModel
# Create your models here.
from uuid import uuid4


class Course(models.Model):
    code_group = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Room(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'room'
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class Lesson(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='lesson_room')
    name = models.CharField(max_length=100)
    code_group = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True,related_name='course_lesson')
    students = models.ManyToManyField(UserModel)
    teacher = models.ForeignKey(UserModel, on_delete=models.SET_NULL,null=True, related_name='course_teacher')
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code_group

    class Meta:
        db_table = 'group'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class Attendance(models.Model):
    schedule = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True,related_name='attendance_lesson')
    student = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True,related_name='attendance_student')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student

    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'


class Order(models.Model):
    code_order = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    amount = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,null=True,)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL,null=True,)
    student = models.ForeignKey(UserModel, on_delete=models.SET_NULL,null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code_order

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
