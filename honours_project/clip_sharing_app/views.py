from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadForm
from pprint import pprint

# Create your views here.

# TODO: have form class rendered on screen using individual fields

def index(request):
    """Homepage view function."""

    if request.method == 'GET':
        form = UploadForm()

        return render(request, 'index.html', context={ 'form': form })
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST['title']
            file = request.FILES["file"]

            filename = file.name
            filesize = file.size // (1024 * 1024)   # Size in MB
            content_type = file.content_type

            print(title, filename, filesize, content_type)

            # TODO create alphanumeric code
            # pprint(vars(file))
            # pprint(dir(file))

            return render(request, 'error.html', context={ 'message': 'Error' })
        

def watch(request):
    video_id: str = request.GET.get('v', None)

    # TODO Implement check for valid video_id

    return render()