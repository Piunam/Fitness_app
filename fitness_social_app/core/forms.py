from django import forms
from .models import Workout, Post, Comment, Progress, Challenge

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description', 'duration']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your fitness journey...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Add a comment...', 'class': 'form-control'}),
        }
        labels = {
            'content': '',
        }

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['workout', 'duration', 'notes', 'calories_burned']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }


class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'goal', 'duration', 'end_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class JoinChallengeForm(forms.Form):
    challenge_id = forms.IntegerField(widget=forms.HiddenInput())
