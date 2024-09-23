from django.contrib import admin
from .models import Video, VideoInstance

# Register your models here.

# admin.site.register(Video)
# admin.site.register(VideoInstance)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'uploaded')

class VideoInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'id', 'expires')