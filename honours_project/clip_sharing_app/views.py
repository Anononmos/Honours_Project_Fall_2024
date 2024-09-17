from django.shortcuts import render

# Create your views here.

def index(request):
    """Homepage view function."""

    return render(request, 'base_generic.html')

def watch(request):
    video_id = request.GET.get('v', None)

    # TODO Implement check for valid video_id