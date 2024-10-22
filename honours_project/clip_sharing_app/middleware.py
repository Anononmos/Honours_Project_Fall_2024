from django.core.cache import cache
from .models import Video

class VideoViewMiddleware:
    """Class responsible for adding views to watch pages."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only count views for valid video ids visiting the watch page

        if request.path == '/watch':
            video_id = request.GET.get('v', None)

            if video_id is None:
                return response
            
            try:
                video = Video.objects.get(id=video_id)

            except Video.DoesNotExist:
                return response 
            
            views = cache.get(video_id, None)

            # If video id is not in cache, add to cache from database

            if views is None:
                views = video.views
                cache.set(video_id, views)

            views += 1
            cache.set(video_id, views)

            video.views = views
            video.save()

        return response      
