import uuid

from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3, max_length=254)
    password = serializers.CharField(min_length=8, max_length=128)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        return value

    @atomic
    def create(self, validated_data):
        user = User(
            username=str(uuid.uuid4()),
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        Token.objects.get_or_create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')
