from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import authenticate

class UserLoginOrCreateView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if a user with the given email exists
        user = authenticate(email=email, password=password)
        if user is not None:
            # User exists, verify the password
            token, created = Token.objects.get_or_create(user=user)
            return Response({'username': user.email, 'token': token.key}, status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({'username': user.email, 'token': token.key}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        return Response({"user":request.user.email})