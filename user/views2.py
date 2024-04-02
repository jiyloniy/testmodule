from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from user.model2 import Student, Company, Teacher
from user.serializers2 import CompanySerializer,StudentSerializer, StudentSerializer2,TeacherSerializer
from user.serializer import UserLoginSerializer
from user.permission2 import IsTeacher, IsStudent, IsCompany,IsTeacherOrCompany,IsStudentOrCompanyOrTeacher
from rest_framework.exceptions import ValidationError,NotAuthenticated


class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
       
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        allowed_fields = ['username', 'password']
        extra_fields = [field for field in request.data.keys() if field not in allowed_fields]
        if extra_fields:
            return Response({'error': f'Unknown fields: {", ".join(extra_fields)}',
                             'status': status.HTTP_400_BAD_REQUEST,
                             },
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )   
        if user is not None:

            if Company.objects.filter(user=user).exists():
                user_type = 'company'
            elif Student.objects.filter(user=user).exists():
                user_type = 'student'
            elif Teacher.objects.filter(user=user).exists():
                user_type = 'teacher'
            else:
                raise ValidationError('user not found')
            if user is not None:
                refresh = RefreshToken.for_user(user)
                refresh['user_type'] = user_type
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
class RegistetCompanyView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e), 'status': status.HTTP_400_BAD_REQUEST,
                             'error2': 'bunday account mavjud '},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        user = User.objects.get(username=serializer.validated_data['username'])
        company = Company.objects.get(user=user)
        if company:
            user_type = 'company'
        if user:
            token_serializer = TokenObtainPairSerializer()
            refresh = token_serializer.get_token(user)
            refresh['user_type'] = user_type
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



class RegistetStudentView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsTeacherOrCompany]

    def permission_denied(self, request, message=None):
        return Response({'error': 'permission denied'}, status=status.HTTP_400_BAD_REQUEST)
    

    error = 'bunday account mavjud '
    
    
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e), 'status': status.HTTP_400_BAD_REQUEST,
                             'error2': 'bunday account mavjud '},
                            status=status.HTTP_400_BAD_REQUEST)
    
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        f_name = serializer.validated_data['f_name']
        l_name = serializer.validated_data['l_name']
        phone = serializer.validated_data['phone']
        phone_2 = serializer.validated_data['phone_2']
        date_of_birth = serializer.validated_data['date_of_birth']
        try:
            if Teacher.objects.filter(user=request.user).exists():
                company = Teacher.objects.get(user=request.user).company
            else:
                company = Company.objects.get(user=request.user)
        except:
            return Response({'error': 'company not found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, password=password)
            student = Student.objects.create(
                user=user,
                f_name=f_name,
                l_name=l_name,
                phone=phone,
                phone_2=phone_2,
                date_of_birth=date_of_birth,
                company=company
            )
            student.save()
        except Exception as e:
            user.delete()
            return Response({'error': str(e), 'status': status.HTTP_400_BAD_REQUEST,
                             'error2': 'bunday student account mavjud '},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        return Response({'message': 'student created','status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    

class RegistetTeacherView(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsCompany]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e), 'status': status.HTTP_400_BAD_REQUEST,
                             'error2': 'bunday account mavjud '},
                            status=status.HTTP_400_BAD_REQUEST)
    
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        phone = serializer.validated_data['phone']
        phone_2 = serializer.validated_data['phone_2']
        date_of_birth = serializer.validated_data['date_of_birth']
        f_name = serializer.validated_data['f_name']
        l_name = serializer.validated_data['l_name']
        try:
            company = Company.objects.get(user=request.user)
        except:
            return Response({'error': 'company not found'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(username=username, password=password)
            teacher = Teacher.objects.create(
                user=user,
                phone=phone,
                phone_2=phone_2,
                date_of_birth=date_of_birth,
                company=company,
                l_name=l_name,
                f_name=f_name
            )
            teacher.save()
        except Exception as e:
            user.delete()
            return Response({'error': str(e), 'status': status.HTTP_400_BAD_REQUEST,
                             'error2': 'bunday teacher account mavjud '},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        return Response({'message': 'teacher created','status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'logout successful'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'token not found'}, status=status.HTTP_400_BAD_REQUEST)
        
def get_user_type(user):
    if Company.objects.filter(user=user).exists():
        user_type = 'company'
    elif Student.objects.filter(user=user).exists():
        user_type = 'student'
    elif Teacher.objects.filter(user=user).exists():
        user_type = 'teacher'
    else:
        raise ValidationError('user not found')
    return user_type



class RefreskTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            user = User.objects.get(id=token['user_id'])
            user_type = get_user_type(user)

            refresh = RefreshToken.for_user(user)
            refresh['user_type'] = user_type
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except:
            return Response({'error': 'token not found'}, status=status.HTTP_400_BAD_REQUEST)
        

# company get and update
class CompanyViewSet(viewsets.ViewSet):
    permission_classes = [IsCompany]

    def list(self, request):
        try:
            company = Company.objects.get(user=request.user)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except:
            return Response({'error': 'company not found'}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        try:
            company = Company.objects.get(user=request.user)
            serializer = CompanySerializer(company, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response({'error': 'company not found'}, status=status.HTTP_400_BAD_REQUEST)
        
# student get and update
class StudentViewSet2(viewsets.ViewSet):
    permission_classes = [IsStudentOrCompanyOrTeacher]

    
        
    def retrieve(self, request, pk=None):
        print('pk', pk)
        try:
            print('request.user', request.user)
            student = Student.objects.get(pk=pk)
            print('student', student)
            serializer = StudentSerializer2(student)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': f'student not found {e}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            phone = serializer.validated_data['phone']
            phone_2 = serializer.validated_data['phone_2']
            date_of_birth = serializer.validated_data['date_of_birth']
            f_name = serializer.validated_data['f_name']
            l_name = serializer.validated_data['l_name']
            
            student.user.username = username
            student.user.set_password(password)
            student.phone = phone
            student.phone_2 = phone_2
            student.date_of_birth = date_of_birth
            student.f_name = f_name
            student.l_name = l_name
            student.save()
            return Response(serializer.data)
        except:
            return Response({'error': 'student not found'}, status=status.HTTP_400_BAD_REQUEST)
    def partial_update (self, request, pk=None):
        try:
            student = Student.objects.get(user=request.user)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            phone = serializer.validated_data['phone']
            phone_2 = serializer.validated_data['phone_2']
            date_of_birth = serializer.validated_data['date_of_birth']
            f_name = serializer.validated_data['f_name']
            l_name = serializer.validated_data['l_name']
            
            student.user.username = username
            student.user.set_password(password)
            student.phone = phone
            student.phone_2 = phone_2
            student.date_of_birth = date_of_birth
            student.f_name = f_name
            student.l_name = l_name
            student.save()
            return Response(serializer.data)
        except:
            return Response({'error': 'student not found'}, status=status.HTTP_400_BAD_REQUEST)
        
    
        
        


from rest_framework import generics

class UpdateStudentView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer2

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Update the User instance
        user = instance.user
        user.username = serializer.validated_data['username']
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Update the Student instance
        return super().update(request, *args, **kwargs)
    
    
    
