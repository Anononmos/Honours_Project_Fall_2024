from django import forms

class UploadForm(forms.Form):

    file = forms.FileField( widget=forms.FileInput(
        attrs={
            'id': 'file-select', 
            'accept': 'video/*', 
            'hidden': True
            }
        ), 
        allow_empty_file=False, 
        required=True, 
        help_text='Select a video file that is at most 50 MB in size and 60s in duration.'
    )
    title = forms.CharField( max_length=50, required=False, widget=forms.TextInput(
        attrs={ 'placeholder': 'Enter a Title' }
        )
    )