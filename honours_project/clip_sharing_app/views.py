from django.http import HttpResponseRedirect  
from django.shortcuts import render
from django.utils import timezone
from django.core import cache
from .models import Video, VideoInstance
from .forms import UploadForm
from .scripts import *

# Create your views here.

def index(request):
    """Homepage view function."""

    error = {
        'message': ''
    }

    if request.method == 'GET':
        form = UploadForm()

        return render(request, 'index.html', context={ 'form': form }, status=200)
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        # Check if form info is safe

        if form.is_valid():
            title = form.cleaned_data['title']
            file = form.cleaned_data['file']
            # title = request.POST['title']
            # file = request.FILES["file"]

            filename: str = file.name

            # Size must be at most 50MB

            if not validate_size(file):
                error['message'] = f'The file uploaded ({filename}) is over {FILE_SIZE} MB in size.'

                return render(request, 'error.html', context=error, status=400)
            
            # Type must be video
            
            if not validate_type(file):
                error['message'] = f'The file uploaded ({filename}) is not a video file.'

                return render(request, 'error.html', context=error, status=400)

            # Duration must be at most 30 seconds.

            try:
                if not validate_duration(file):
                    error['message'] = f'The file uploaded ({filename}) is over {DURATION} seconds in duration.'

                    return render(request, 'error.html', context=error, status=400)

            # Issues with ffprobe

            except Exception as err:
                print(err)

                error['message'] = f'The file uploaded ({filename}) cannot have its duration accessed.'

                return render(request, 'error.html', context=error, status=400)

            # Create objects for saving in the database

            video = Video.objects.create(title=title)
            video.save()

            instance = VideoInstance.objects.create(video=video, file=file)
            instance.save()
    
            return HttpResponseRedirect(f'/watch?v={video.id}')
        
        else:
            error['message'] = form.errors.as_text()

            return render(request, 'error.html', context=error, status=400)

    else:    
        error['message'] = 'Bad request method.'

        return render(request, 'error.html', context=error, status=400)
        

def watch(request):
    """Returns watch page corresponding with a given video id as a query parameter."""

    video_id: str = request.GET.get('v', None)

    error = {
        'message': ''
    }

    if video_id is None:
        error['message'] = f'No video id is provided.'

        return render(request, 'error.html', context=error)

    try:
        video = Video.objects.get(pk=video_id)
        instance = VideoInstance.objects.get(video__id=video_id)

    except (Video.DoesNotExist, VideoInstance.DoesNotExist):
        error['message'] = f'The video with id ({video_id}) does not exist.'

        return render(request, 'error.html', context=error, status=404)
    
    # Check if the current time is after expiry time

    if timezone.now() >= video.expires:
        error['message'] = f'The video with id ({video_id}) has expired.'

        return render(request, 'error.html', context=error, status=403)

    context = {
        'title': video.title, 
        'uploaded': video.uploaded, 
        'views': video.views, 
        'url': instance.file.url
    }

    return render(request, 'watch.html', context=context, status=200)