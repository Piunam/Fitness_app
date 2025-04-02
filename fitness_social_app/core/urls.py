from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('workout-plans/', views.workout_plans, name='workout_plans'),
    path('add-workout/', views.add_workout, name='add_workout'),
    path('edit-workout/<int:pk>/', views.edit_workout, name='edit_workout'),
    path('delete-workout/<int:pk>/', views.delete_workout, name='delete_workout'),
    path('log-workout/', views.log_workout, name='log_workout'),

    # Social Feed URLs
    path('social-feed/', views.social_feed, name='social_feed'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('discover/', views.discover_users, name='discover_users'),

    path('achievements/', views.achievements_list, name='achievements'),
    path('challenges/', views.challenges_list, name='challenges'),
    
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]



