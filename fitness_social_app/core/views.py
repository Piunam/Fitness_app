from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Workout, Progress, SocialConnection
from django.contrib.auth.models import User
from .forms import WorkoutForm



@login_required
def dashboard(request):
    user_workouts = Workout.objects.filter(user=request.user)
    user_progress = Progress.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'workouts': user_workouts, 'progress': user_progress})


# @login_required
# def workout_plans(request):
#     all_workouts = Workout.objects.all()
#     return render(request, 'workout_plans.html', {'workouts': all_workouts})

@login_required
def workout_plans(request):
    workouts = Workout.objects.filter(user=request.user)  # Show only the logged-in user's workouts
    return render(request, 'workout_plans.html', {'workouts': workouts})


@login_required
def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user  # Assign the logged-in user as the creator
            workout.save()
            return redirect('workout_plans')
    else:
        form = WorkoutForm()
    return render(request, 'add_workout.html', {'form': form})

@login_required
def edit_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('workout_plans')
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'edit_workout.html', {'form': form})

@login_required
def delete_workout(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        workout.delete()
        return redirect('workout_plans')
    return render(request, 'delete_workout.html', {'workout': workout})




@login_required
def social_feed(request):
    following = SocialConnection.objects.filter(follower=request.user).values_list('following', flat=True)
    feed_posts = Progress.objects.filter(user__in=following).order_by('-completed_on')
    return render(request, 'social_feed.html', {'feed_posts': feed_posts})
