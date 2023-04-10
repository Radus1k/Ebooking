from django import forms
from .models import HotelRoom

"""
Model form used to edit a hotel room
"""
class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        # fields = ['name', 'description', 'price', 'capacity', 'image']
        fields = [ 'price', 'image', ]

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            # 'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'capacity': forms.NumberInput(attrs={'class': 'form-control'}),      
        }

class AddHotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        fields = ['hotel', 'image', 'beds', 'has_terrace', 'has_kitchen', 'has_tv', 'has_fridge', 'floor_no', 'price']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['hotel'].queryset = user.profile.hotels.all()