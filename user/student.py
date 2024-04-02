
from user.studentserial import StudentSerializerTest
from user.model2 import Student
from user.permission2 import IsStudentOrCompanyOrTeacher,IsTeacherOrCompany

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from user.model2 import Student, Company, Teacher

from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
@action(detail=False, methods=['get'], permission_classes=[IsTeacherOrCompany])
def get_student(request):
    student = Student.objects.all()
    serializer = StudentSerializerTest(student, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# @action(detail=True, methods=['get'], permission_classes=[IsStudentOrCompanyOrTeacher])
# def get_student_by_id( request, pk=None):
#     student = Student.objects.get(id=pk)
#     serializer = StudentSerializerTest(student)
#     return Response(serializer.data, status=status.HTTP_200_OK)



def get_company(user):
    if Company.objects.filter(user=user).exists():
        return Company.objects.get(user=user)
    if Teacher.objects.filter(user=user).exists():
        return Teacher.objects.get(user=user).company
    if Student.objects.filter(user=user).exists():
        return Student.objects.get(user=user).company
    raise NotFound(detail='Company not found', code=status.HTTP_404_NOT_FOUND)


# @action(detail=True, methods=['put'], permission_classes=[IsStudentOrCompanyOrTeacher])
# def update_student(request, pk=None):
#     try:
#         student = Student.objects.get(id=pk)
#     except Student.DoesNotExist:
#         return Response(
#             {'error': 'Student does not exist',
#              'status': status.HTTP_404_NOT_FOUND},
#              status=status.HTTP_404_NOT_FOUND
#         )
#     company = get_company(request.user)
#     if company != student.company:
#         return Response(
#             {'error': 'You are not allowed to update this student',
#              'status': status.HTTP_403_FORBIDDEN},
#              status=status.HTTP_403_FORBIDDEN
#         )
    
#     serializer = StudentSerializerTest(student, data=request.data)
#     serializer.is_valid(raise_exception=True)
#     username = serializer.validated_data['username']
#     password = serializer.validated_data['password']
#     f_name = serializer.validated_data['f_name']
#     l_name = serializer.validated_data['l_name']
#     phone = serializer.validated_data['phone']
#     phone_2 = serializer.validated_data['phone_2']
#     date_of_birth = serializer.validated_data['date_of_birth']

#     user = student.user
#     if user.username != username:
#         user.username = username
#     if password:
#         user.set_password(password)
#     user.save()
#     student.company = company
#     if f_name:

#         student.f_name = f_name
#     if l_name:
#         student.l_name = l_name
#     if phone:
#         student.phone = phone
#     if phone_2:
    
#         student.phone_2 = phone_2
#     if date_of_birth:
#         student.date_of_birth = date_of_birth
#     student.save()
    
#     return Response(serializer.data, status=status.HTTP_200_OK)
    



# delete student
@action(detail=True, methods=['delete'], permission_classes=[IsTeacherOrCompany])
def delete_student(request, pk=None):
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student does not exist',
             'status': status.HTTP_404_NOT_FOUND},
             status=status.HTTP_404_NOT_FOUND
        )
    company = get_company(request.user)
    if company != student.company:
        return Response(
            {'error': 'You are not allowed to delete this student',
             'status': status.HTTP_403_FORBIDDEN},
             status=status.HTTP_403_FORBIDDEN
        )
    student.delete()
    return Response(
        {'message': 'Student deleted successfully',
         'status': status.HTTP_200_OK},
         status=status.HTTP_200_OK
    )
from rest_framework.decorators import api_view, permission_classes
@api_view(['GET'])
@permission_classes([IsTeacherOrCompany])
def get_student(request):
    try:
        company = get_company(request.user)
    except Company.DoesNotExist:
        return Response(
            {'error': 'Company does not exist',
             'status': status.HTTP_404_NOT_FOUND},
             status=status.HTTP_404_NOT_FOUND
        )
    try:
        student = Student.objects.filter(company=company)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student does not exist',
             'status': status.HTTP_404_NOT_FOUND},
             status=status.HTTP_404_NOT_FOUND
        )
    serializer = StudentSerializerTest(student, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsStudentOrCompanyOrTeacher])
def get_student_by_id(request, pk=None):
    company = get_company(request.user)
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student does not exist',
             'status': status.HTTP_404_NOT_FOUND},
             status=status.HTTP_404_NOT_FOUND
        )
    if student.company != company:
        return Response(
            {'error': 'You are not allowed to view this student',
             'status': status.HTTP_403_FORBIDDEN},
             status=status.HTTP_403_FORBIDDEN
        )
    serializer = StudentSerializerTest(student)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsStudentOrCompanyOrTeacher])
def update_student(request, pk=None):
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student does not exist',
             'status': status.HTTP_404_NOT_FOUND},
             status=status.HTTP_404_NOT_FOUND
        )
    company = get_company(request.user)
    if company != student.company:
        return Response(
            {'error': 'You are not allowed to update this student',
             'status': status.HTTP_403_FORBIDDEN},
             status=status.HTTP_403_FORBIDDEN
        )
    serializer = StudentSerializerTest(student, data=request.data,partial=True)
    serializer.is_valid(raise_exception=True)
    
   
    
    validated_data = serializer.validated_data
    if not any(
        [
            validated_data.get('user', {}).get('username', None),
            validated_data.get('password', None),
            
            validated_data.get('f_name', None),
            validated_data.get('l_name', None),
            validated_data.get('phone', None),
            validated_data.get('phone_2', None),
            validated_data.get('date_of_birth', None),
        ]
    ):
        return Response(
            {'error': 'No data to update',
             'status': status.HTTP_400_BAD_REQUEST},
             status=status.HTTP_400_BAD_REQUEST
        )
    user = student.user
    username = validated_data.get('user', {}).get('username', user.username)
    password = validated_data.get('password', None)
    
    if user.username != username:
        user.username = username
    if password:
        user.set_password(password)
    user.save()

    student.company = company
    student.f_name = validated_data.get('f_name', student.f_name)
    student.l_name = validated_data.get('l_name', student.l_name)
    student.phone = validated_data.get('phone', student.phone)
    student.phone_2 = validated_data.get('phone_2', student.phone_2)
    student.date_of_birth = validated_data.get('date_of_birth', student.date_of_birth)
    student.save()
    return Response(
        {'message': 'Student updated successfully',
            'status': status.HTTP_200_OK,
            'data': serializer.data
         },
            status=status.HTTP_200_OK
    )

