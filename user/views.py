from django.contrib.auth.models import User

from rest_framework import generics
from user.models import User as UserModel

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from user.serializer import UserLoginSerializer, UserRegisterSerializer
from education.permissions import IsTeacher, IsStudent, IsAdmin


class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
  
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            refresh['user_type'] = UserModel.objects.get(user=user).user_type
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAdmin, IsTeacher]

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
        Userm = UserModel.objects.get(user=user)
        if user:
            token_serializer = TokenObtainPairSerializer()
            refresh = token_serializer.get_token(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_type': Userm.user_type
            }
            return Response(data)
        else:
            return Response({'error': 'Invalid credentials', 'xatolik': 'xatolik'}, status=status.HTTP_400_BAD_REQUEST)
