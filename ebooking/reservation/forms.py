from .models import Reservation
from django import forms
from hotels.models import HotelRoom
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User

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

    def __init__(self, *args, **kwargs):
        is_admin = kwargs.pop('is_admin', False)
        print("IS ADMIN ? :", is_admin)
        super().__init__(*args, **kwargs)
        if not is_admin: # Status and user only for admins
            self.fields.pop('status')
        else:
            self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all())
            
