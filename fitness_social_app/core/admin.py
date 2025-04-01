from django.contrib import admin
from .models import Profile, Workout, Progress, SocialConnection,  Post, Comment, Like

admin.site.register(Profile)
# admin.site.register(Workout)
admin.site.register(Progress)
admin.site.register(SocialConnection)


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'duration', 'date_created')
    search_fields = ('name', 'user__username')

admin.site.register(Workout, WorkoutAdmin)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_preview', 'created_at')
    search_fields = ('user__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content_preview', 'created_at')
    search_fields = ('user__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username',)


