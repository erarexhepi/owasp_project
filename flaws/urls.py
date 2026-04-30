from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('profile/<int:user_id>/', views.profile),
    path('search/', views.search),
    path('login/', views.login_view),
    path('transfer/', views.transfer),
]