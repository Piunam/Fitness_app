from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workout, Progress, SocialConnection, Post, Comment, Like, User, Profile, Streak, Achievement, Challenge, ChallengeParticipation
from django.contrib.auth.models import User
from .forms import WorkoutForm, PostForm, CommentForm, ProgressForm, ChallengeForm
from django.db.models import Q
from django.db.models import Count, Sum, Exists, OuterRef
from django.utils import timezone
import datetime
from django.contrib.auth.forms import UserCreationForm
import random





def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful sign-up
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



@login_required
def dashboard(request):
    # Get the current user's profile
    try:
        profile = request.user.profile
    except:
        profile = Profile.objects.create(user=request.user)
    
    # Get upcoming workouts
    today = timezone.now().date()
    upcoming_workouts = Workout.objects.filter(user=request.user, date_created__gte=today).order_by('date_created')[:5]

    # Get recent progress (last 30 days)
    thirty_days_ago = timezone.now() - datetime.timedelta(days=30)
    recent_progress = Progress.objects.filter(
        user=request.user, 
        completed_on__gte=thirty_days_ago
    ).order_by('-completed_on')
    
    # Calculate workout stats
    total_workouts = recent_progress.count()
    total_duration = recent_progress.aggregate(Sum('duration'))['duration__sum'] or 0
    
    # Get workout categories and counts for chart
    workout_categories = recent_progress.values('workout__name').annotate(
        count=Count('workout__name')
    ).order_by('-count')[:5]
    
    # Get recent activity from connections (people the user follows)
    following = SocialConnection.objects.filter(follower=request.user).values_list('following', flat=True)
    recent_activities = Progress.objects.filter(
        user__in=following
    ).select_related('user', 'workout').order_by('-completed_on')[:5]
    
    # Prepare workout types for the quick log form
    all_workouts = Workout.objects.filter(user=request.user)
    
    # Format data for chart.js
    chart_labels = [item['workout__name'] for item in workout_categories]
    chart_data = [item['count'] for item in workout_categories]
    
    
    # Add motivation features
    try:
        streak = Streak.objects.get(user=request.user)
    except Streak.DoesNotExist:
        streak = Streak.objects.create(user=request.user)
    
    achievements = Achievement.objects.filter(user=request.user).order_by('-unlocked_at')[:3]
    active_challenges = Challenge.objects.filter(
        participants=request.user,
        challengeparticipation__completed=False
    )
    
    
    # Motivational messages
    MOTIVATION_PHRASES = [
        "Every rep counts! 💪",
        "Consistency is key! 🔑",
        "You're stronger than you think! 💥",
        "Progress, not perfection! 📈"
    ]
    
    
    return render(request, 'dashboard.html', {
        'profile': profile,
        'upcoming_workouts': upcoming_workouts,
        'recent_progress': recent_progress,
        'total_workouts': total_workouts,
        'total_duration': total_duration,
        'recent_activities': recent_activities,
        'all_workouts': all_workouts,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'streak': streak,
        'achievements': achievements,
        'active_challenges': active_challenges,
        'motivation_phrase': random.choice(MOTIVATION_PHRASES)
    })


@login_required
def log_workout(request):
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            
            # Update active challenges
            active_participations = ChallengeParticipation.objects.filter(
                user=request.user,
                completed=False
            )
            
            for participation in active_participations:
                if participation.challenge.is_active:
                    participation.progress += 1
                    if participation.progress >= participation.challenge.goal:
                        participation.completed = True
                        messages.success(
                            request, 
                            f"Congratulations! You've completed the '{participation.challenge.title}' challenge!"
                        )
                    participation.save()
            
            return redirect('dashboard')
    return redirect('dashboard')


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
    # Get users that the current user is following
    following = SocialConnection.objects.filter(follower=request.user).values_list('following', flat=True)
    
    # Get posts from users that the current user is following, plus their own posts
    feed_posts = Post.objects.filter(user__in=list(following) + [request.user.id])
    
    # Mark posts that the current user has liked
    for post in feed_posts:
        post.is_liked_by_user = Like.objects.filter(user=request.user, post=post).exists()
    
    # Form handling for creating new posts
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('social_feed')
    else:
        form = PostForm()
    
    # Create comment form for use in template
    comment_form = CommentForm()
    
    return render(request, 'social_feed.html', {
        'feed_posts': feed_posts,
        'form': form,
        'comment_form': comment_form
    })



@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Handle comments
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'post_detail.html', {
        'post': post,
        'form': form
    })

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # User already liked the post, so unlike it
        like.delete()
    
    next_url = request.GET.get('next', 'social_feed')
    return redirect(next_url)

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    
    # Check if the current user is following this user
    is_following = SocialConnection.objects.filter(
        follower=request.user,
        following=user
    ).exists()
    
    return render(request, 'user_profile.html', {
        'profile_user': user,
        'posts': posts,
        'is_following': is_following
    })


@login_required
def discover_users(request):
    # Create profile for current user if it doesn't exist
    try:
        user_profile = request.user.profile
    except:
        user_profile = Profile.objects.create(user=request.user)
    
    # Get all users except the current user
    users = User.objects.exclude(id=request.user.id)
    
    # Get the users that the current user is already following
    following_ids = SocialConnection.objects.filter(follower=request.user).values_list('following', flat=True)
    
    # Use a more robust filter
    similar_users = users.exclude(id__in=following_ids)
    
    # If the current user has a fitness goal, filter by that
    if hasattr(user_profile, 'fitness_goal') and user_profile.fitness_goal:
        similar_users = similar_users.filter(
            profile__fitness_goal=user_profile.fitness_goal
        ).distinct()
    
    return render(request, 'discover_users.html', {
        'users': similar_users,
        'following_ids': list(following_ids),
    })




@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    # Prevent self-following
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
        return redirect('user_profile', username=username)

    # Check if already following
    connection, created = SocialConnection.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if created:
        messages.success(request, f"You are now following {username}.")
    else:
        # Unfollow if already following
        connection.delete()
        messages.success(request, f"You have unfollowed {username}.")

    return redirect('discover_users')



@login_required
def achievements_list(request):
    achievements = Achievement.objects.filter(user=request.user).order_by('-unlocked_at')
    return render(request, 'achievements.html', {'achievements': achievements})


@login_required
def challenges_list(request):
    # Get all challenges
    all_challenges = Challenge.objects.all().order_by('-start_date')
    
    # Mark which challenges the user has joined
    for challenge in all_challenges:
        challenge.user_joined = ChallengeParticipation.objects.filter(
            user=request.user, 
            challenge=challenge
        ).exists()
        
        if challenge.user_joined:
            participation = ChallengeParticipation.objects.get(
                user=request.user, 
                challenge=challenge
            )
            challenge.user_progress = participation.progress
            challenge.user_progress_percentage = participation.progress_percentage
    
    # Sort challenges: user's active challenges first
    user_active = [c for c in all_challenges if c.user_joined and c.is_active]
    other_active = [c for c in all_challenges if not c.user_joined and c.is_active]
    completed = [c for c in all_challenges if c.user_joined and not c.is_active]
    
    context = {
        'user_active_challenges': user_active,
        'other_active_challenges': other_active,
        'completed_challenges': completed,
    }
    
    return render(request, 'challenges.html', context)

@login_required
def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.creator = request.user
            challenge.save()
            
            # Creator automatically joins their own challenge
            ChallengeParticipation.objects.create(
                user=request.user,
                challenge=challenge
            )
            
            messages.success(request, "Challenge created successfully!")
            return redirect('challenges')
    else:
        form = ChallengeForm()
    
    return render(request, 'create_challenge.html', {'form': form})

@login_required
def join_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    
    if not challenge.is_active:
        messages.error(request, "This challenge is no longer active.")
        return redirect('challenges')
    
    # Check if user already joined
    already_joined = ChallengeParticipation.objects.filter(
        user=request.user,
        challenge=challenge
    ).exists()
    
    if already_joined:
        messages.info(request, "You are already participating in this challenge.")
    else:
        ChallengeParticipation.objects.create(
            user=request.user,
            challenge=challenge
        )
        messages.success(request, f"You've joined the '{challenge.title}' challenge!")
    
    return redirect('challenges')

@login_required
def leave_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    participation = get_object_or_404(
        ChallengeParticipation, 
        user=request.user,
        challenge=challenge
    )
    
    if request.method == 'POST':
        participation.delete()
        messages.success(request, f"You've left the '{challenge.title}' challenge.")
        return redirect('challenges')
    
    return render(request, 'leave_challenge.html', {'challenge': challenge})

@login_required
def update_challenge_progress(request, challenge_id):
    challenge = get_object_or_404(Challenge, pk=challenge_id)
    participation = get_object_or_404(
        ChallengeParticipation, 
        user=request.user,
        challenge=challenge
    )
    
    if request.method == 'POST':
        # Increment progress by 1
        participation.progress += 1
        
        # Check if challenge is completed
        if participation.progress >= challenge.goal:
            participation.completed = True
            messages.success(request, f"Congratulations! You've completed the '{challenge.title}' challenge!")
        else:
            messages.success(request, f"Progress updated for '{challenge.title}' challenge!")
            
        participation.save()
    
    return redirect('challenges')
