from .models import Reservation
from django import forms
from hotels.models import HotelRoom
from django.forms.widgets import SelectDateWidget

class ReservationForm(forms.ModelForm):
    begin_at = forms.DateField(widget=SelectDateWidget())
    ends_at = forms.DateField(widget=SelectDateWidget())
    class Meta:
        model = Reservation
        exclude = ('user',)
        widgets = {
                'begin_at': forms.SelectDateWidget(),
                'ends_at': forms.SelectDateWidget(),
            }    
        phone_no = forms.CharField(label="Phone number") 
