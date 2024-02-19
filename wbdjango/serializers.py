from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import ColorUser, PostFile
from rest_framework.serializers import ModelSerializer

from rest_framework.request import Request


User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'is_active', 'password')


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad token')


class ColorUserSerializer(serializers.ModelSerializer):
    color = serializers.BooleanField(allow_null=True)
    date = serializers.DateField(allow_null=True)

    class Meta:
        model = ColorUser
        fields = ['id', 'user', 'color', 'date']

    def create(self, validated_data):
        user = validated_data['user']
        date = validated_data['date']

        # Пытаемся найти запись с заданным пользователем и датой
        instance, created = ColorUser.objects.get_or_create(
            user=user,
            date=date,
            defaults={'color': validated_data['color']}
        )

        # Если запись уже существует, обновляем цвет
        if not created:
            instance.color = validated_data['color']
            instance.save()

        return instance

class PostSerializer(ModelSerializer):
    class Meta:
        model = PostFile
        fields = ('name', 'file')


class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ['name', 'file']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


