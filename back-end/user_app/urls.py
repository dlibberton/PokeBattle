from django.urls import path
from user_app.views import UserLoginOrCreateView

urlpatterns = [
    path('', UserLoginOrCreateView.as_view(), name='login_or_create'),
]