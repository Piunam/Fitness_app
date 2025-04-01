from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fitness_goal = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# class Workout(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.name} - {self.user.username}"

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who created it
    name = models.CharField(max_length=100)  # Name of the workout plan
    description = models.TextField()  # Description of the workout plan
    duration = models.IntegerField(help_text="Duration in minutes")  # Duration of the workout
    date_created = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):
        return f"{self.name} - {self.user.username}"


# class Progress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
#     completed_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.workout.name} - {self.completed_on}"

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_entries')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed_on = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    notes = models.TextField(blank=True, null=True)
    calories_burned = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.workout.name} ({self.completed_on.strftime('%Y-%m-%d')})"


class SocialConnection(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}..."
    
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} on {self.post.id}: {self.content[:20]}..."
    
    class Meta:
        ordering = ['created_at']

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        
    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"
