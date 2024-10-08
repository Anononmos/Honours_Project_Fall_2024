from django import forms

class UploadForm(forms.Form):
    file = forms.FileField( widget=forms.FileInput(
        attrs={
            'id': 'file-select', 
            'accept': 'video/*', 
            'hidden': True
            }
        )
    )
    title = forms.CharField( max_length=50, required=False, widget=forms.TextInput(
        attrs={ 'placeholder': 'Enter a Title' }
        )
    )