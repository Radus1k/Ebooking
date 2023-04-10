from .models import Reservation
from django import forms
from hotels.models import HotelRoom

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ()
    phone_no = forms.CharField(label="Phone number") 
