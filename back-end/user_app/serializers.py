from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
        