from django.urls import path
from home_app.views import HomePageView, TutorialPageView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('tutorial/', TutorialPageView.as_view(), name='tutorial'),
]