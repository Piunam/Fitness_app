from django.contrib import admin
from .models import Profile, Workout, Progress, SocialConnection

admin.site.register(Profile)
# admin.site.register(Workout)
admin.site.register(Progress)
admin.site.register(SocialConnection)


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'duration', 'date_created')
    search_fields = ('name', 'user__username')

admin.site.register(Workout, WorkoutAdmin)