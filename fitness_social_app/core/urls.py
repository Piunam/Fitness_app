from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('workout-plans/', views.workout_plans, name='workout_plans'),
    path('add-workout/', views.add_workout, name='add_workout'),
    path('edit-workout/<int:pk>/', views.edit_workout, name='edit_workout'),
    path('delete-workout/<int:pk>/', views.delete_workout, name='delete_workout'),
    path('social-feed/', views.social_feed, name='social_feed'),
]


