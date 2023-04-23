from .models import Reservation
from django import forms
from hotels.models import HotelRoom
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User

class ReservationForm(forms.ModelForm):
    begin_at = forms.DateField(widget=SelectDateWidget())
    ends_at = forms.DateField(widget=SelectDateWidget())
    # edit_date_warning = "Kindly note that the reservation date can only be edited by at least 72 hours prior to the scheduled beginning date. Any changes requested beyond this timeframe may not be accommodated. Thank you for your attention to this policy!"
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
        super().__init__(*args, **kwargs)
        if not is_admin: # Status and user only for admins
            self.fields.pop('status')
        else:
            self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all())
            
        # self.fields['warning_button'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control warning', 'title': self.warning_text}))    
