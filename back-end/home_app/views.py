from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class HomePageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'user': request.user.email})

class TutorialPageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'user': request.user.email})
    
