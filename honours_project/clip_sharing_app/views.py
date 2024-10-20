from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Video, VideoInstance
from .forms import UploadForm
from .scripts import *

# Create your views here.

# TODO: have form class rendered on screen using individual fields

def index(request):
    """Homepage view function."""

    if request.method == 'GET':
        form = UploadForm()

        return render(request, 'index.html', context={ 'form': form })
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        error = {
            'message': ''
        }

        if form.is_valid():
            title = form.cleaned_data['title']
            file = form.cleaned_data['file']
            # title = request.POST['title']
            # file = request.FILES["file"]

            filename: str = file.name

            if not validate_size(file):
                context['message'] = f'The file uploaded ({filename}) is over {FILE_SIZE} MB in size.'

                return render(request, 'error.html', context=error, status=415)
            
            if not validate_type(file):
                context['message'] = f'The file uploaded ({filename}) is not a video file.'

                return render(request, 'error.html', context=error, status=415)

            try:
                if not validate_duration(file):
                    context['message'] = f'The file uploaded ({filename}) is over {DURATION} seconds in duration.'

                    return render(request, 'error.html', context=error, status=415)

            except Exception as err:
                print(err)

                context = {
                    'message': f'The file uploaded ({filename}) cannot have its duration accessed.'
                }

                return render(request, 'error.html', context=error, status=400)

            # Create objects for saving in the database

            video = Video.objects.create(title=title)
            video.save()

            instance = VideoInstance.objects.create(video=video, file=file)
            instance.save()
    
            return HttpResponseRedirect(f'/watch?v={video.id}')
        

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

    except:
        error['message'] = f'The video with id ({video_id}) does not exist.'

        return render(request, 'error.html', context=error, status=404)
    
    if timezone.now() >= video.expires + timedelta(minutes=10):
        error['message'] = f'The video with id ({video_id}) has expired.'

        return render(request, 'error.html', context=error, status=401)
    
    context = {
        'title': video.title, 
        'uploaded': video.uploaded, 
        'views': video.views, 
        'url': instance.file.url
    }

    return render(request, 'watch.html', context=context)