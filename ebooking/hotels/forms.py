from django import forms
from .models import HotelRoom

class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom  
        fields = ('image', 'beds',)