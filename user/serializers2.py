from rest_framework import serializers
from user.model2 import Student, Company, Teacher
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        read_only_fields = ('id',)
        depth = 1

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],password=validated_data['password'])
        return user
    
    def validate(self, attrs):
        username = attrs.get('username', '')
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('Username is already in use')})
        return super().validate(attrs)
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation.pop('user')
    #     return representation

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance
    

class CompanySerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True,source='user.username')
    password = serializers.CharField(write_only=True,source='user.password')

    class Meta:
        model = Company
        fields = ('id', 'name', 'location', 'logo', 'username', 'password')
        # logo required


        read_only_fields = ('id',)
        depth = 1
        



    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        try:
            user = User.objects.create_user(username=username,password=password)
            
            company = Company.objects.create(
                user=user,
                name=validated_data['name'],
                location=validated_data['location'],
                logo=validated_data['logo']
            )
        except Exception as e:
            user.delete()
            raise e
        return company
    
    def validate(self, attrs):
        username = attrs.get('username', '')
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('Username is already in use')})
        return super().validate(attrs)
    
    

    def update(self, instance, validated_data):
        username = validated_data.get('username', instance.user.username)
        password = validated_data.get('password', instance.user.password)
        instance.user.username = username
        instance.user.set_password(password)
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()
        return instance
    
class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, instance=None, data=..., **kwargs):
        user_company = kwargs.pop('user_company', None)

        super().__init__(instance=instance, data=data, **kwargs)
        

    class Meta:
        model = Student
        fields = ('id',   'username', 'password', 'phone', 'phone_2', 'date_of_birth','f_name', 'l_name')
        read_only_fields = ('id',)
        depth = 1
        ref_name = 'StudentSerilar1312'
    def validate(self, attrs):
        username = attrs.get('username', '')
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('Username is already in use')})
        return super().validate(attrs)

class UserSerializer2(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ('username', 'password')
        read_only_fields = ('id',)
        depth = 1

class StudentSerializer2(serializers.ModelSerializer):
    # user = UserSerializer2()
    username=serializers.CharField(source='user.username')
    password=serializers.CharField(source='user.password')
    confrim_password = serializers.CharField(write_only=True)
    class Meta:
        model = Student
        fields = ('id', 'phone', 'phone_2', 'date_of_birth','f_name', 'l_name', 'username', 'password')
        read_only_fields = ('id',)
        depth = 1
        ref_name = 'StudentSerilar'
    def validate(self, attrs):
        username = attrs.get('user')['username']
        password = attrs.get('user')['password']
        confrim_password = attrs.get('confrim_password')
        if password != confrim_password:
            raise serializers.ValidationError({'password': ('Password must match')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('Username is already in use')})
        return super().validate(attrs)













class TeacherSerializer(serializers.ModelSerializer):
   
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Teacher
        fields = ('id',  'username', 'password', 'phone', 'phone_2', 'date_of_birth','f_name', 'l_name', 'username', 'password')
        read_only_fields = ('id',)
        depth = 1

    def validate(self, attrs):
        username = attrs.get('username', '')
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': ('Username is already in use')})
        return super().validate(attrs)
    
    