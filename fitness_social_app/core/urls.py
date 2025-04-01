from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('workout-plans/', views.workout_plans, name='workout_plans'),
    path('social-feed/', views.social_feed, name='social_feed'),
]
