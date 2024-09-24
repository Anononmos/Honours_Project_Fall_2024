from django.contrib import admin
from .models import Video, VideoInstance

# Register your models here.

# admin.site.register(Video)
# admin.site.register(VideoInstance)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'expires', 'uploaded', 'title', 'views')

@admin.register(VideoInstance)
class VideoInstanceAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'get_expiry', 'get_uploaded', 'get_title', 'get_views')