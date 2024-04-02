from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import User
from .models import User as UserProfile, Lead
from django.contrib.auth import authenticate
from rest_framework import status

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    user_type = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'phone', 'address', 'user_type', 'username', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        user_profile = UserProfile.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            user_type=validated_data['user_type']
        )
        return user_profile

    def validate(self, attrs):
        username = attrs.get('username')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'phone': 'Phone number already exists'})
        return attrs

    def update(self, instance, validated_data):
        user = instance.auth_user
        user_profile = instance
        user_profile_data = validated_data.pop('user_profile', None)
        user = super().update(instance, validated_data)
        if user_profile_data:
            user_profile.user_type = user_profile_data['user_type']
            user_profile.save()
        return user_profile

    def save(self, **kwargs):
        super().save(**kwargs)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({'message': 'Invalid username or password'})

        # get exra fields
        extra_fields = set(attrs.keys()) - set(self.fields.keys())
        print(extra_fields)
        if extra_fields:
            raise serializers.ValidationError({'non_field_errors': [f"Unknown fields: {', '.join(extra_fields)}"]})

        return attrs


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'first_name', 'last_name', 'phone', 'phone_2', 'address')
        read_only_fields = ('id', 'created_at', 'updated_at')
