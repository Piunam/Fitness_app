from django.contrib import admin
from .models import Profile, Workout, Progress, SocialConnection

admin.site.register(Profile)
admin.site.register(Workout)
admin.site.register(Progress)
admin.site.register(SocialConnection)
