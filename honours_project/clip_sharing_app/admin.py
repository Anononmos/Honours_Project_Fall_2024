from django.contrib import admin
from .models import Video, VideoInstance

# Register your models here.

# admin.site.register(Video)
# admin.site.register(VideoInstance)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'uploaded')

@admin.register(VideoInstance)
class VideoInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'id', 'expires')