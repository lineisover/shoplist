from django import forms

from .models import UserSpace


class UserSpaceForm(forms.ModelForm):
    class Meta:
        model = UserSpace
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название пространства',
                'class': 'input-field',
            }),
        }
        labels = {
            'name': '',
        }
