from django.urls import path
from game_app.views import ShopPageView, StatsPageView, BattlePageView

urlpatterns = [
    path('shop/', ShopPageView.as_view(), name='shop'),
    path('battle/', BattlePageView.as_view(), name='battle'),
    path('stats/', StatsPageView.as_view(), name='stats')
]