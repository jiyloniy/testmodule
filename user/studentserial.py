from rest_framework import serializers
from user.model2 import Student
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class StudentSerializerTest(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, source='user.username')
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Student
        fields = ('id', 'f_name','user', 'l_name', 'phone', 'phone_2', 'date_of_birth', 'company', 'username', 'password', 'password2')
        read_only_fields = ('id',)
        depth = 1

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        print(password)
        print(password2)
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        return attrs
    
    
