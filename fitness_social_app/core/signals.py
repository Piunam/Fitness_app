from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Progress, Streak, Achievement

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Progress)
def handle_motivational_features(sender, instance, created, **kwargs):
    if created:
        # Update streak
        streak, _ = Streak.objects.get_or_create(user=instance.user)
        streak.update_streak()
        
        # Check achievements
        total_workouts = Progress.objects.filter(user=instance.user).count()
        if total_workouts == 1:
            Achievement.objects.create(
                user=instance.user,
                name="First Workout!",
                description="Completed your first workout",
                icon="fa-solid fa-dumbbell"
            )
        elif total_workouts % 10 == 0:
            Achievement.objects.create(
                user=instance.user,
                name=f"{total_workouts} Workouts Completed",
                description=f"Consistency champion! {total_workouts} workouts logged",
                icon="fa-solid fa-trophy"
            )
