from django import forms
from .models import AnonymousMessage

class AnonymousMessageForm(forms.ModelForm):
    class Meta:
        model = AnonymousMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'nimadur...',
                'class': 'form-control',  
                'rows': 4
            })
        }
