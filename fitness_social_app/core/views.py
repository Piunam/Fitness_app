from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Workout, Progress, SocialConnection
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    user_workouts = Workout.objects.filter(user=request.user)
    user_progress = Progress.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'workouts': user_workouts, 'progress': user_progress})


@login_required
def workout_plans(request):
    all_workouts = Workout.objects.all()
    return render(request, 'workout_plans.html', {'workouts': all_workouts})

@login_required
def social_feed(request):
    following = SocialConnection.objects.filter(follower=request.user).values_list('following', flat=True)
    feed_posts = Progress.objects.filter(user__in=following).order_by('-completed_on')
    return render(request, 'social_feed.html', {'feed_posts': feed_posts})
