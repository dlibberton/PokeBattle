from django.urls import path
from user_app.views import UserLoginOrCreateView, LogOut

urlpatterns = [
    path('', UserLoginOrCreateView.as_view(), name='login_or_create'),
    path('users/logout/', LogOut.as_view(), name='logout')
]