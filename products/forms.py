from django import forms
from django import forms
from .models import Profiles

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['full_name', 'street', 'city', 'state', 'zipcode', 'telephone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
