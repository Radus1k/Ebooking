from django import forms
from .models import HotelRoom, Review

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['hotel', 'rating', 'text']
        
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating

    def clean_text(self):
        text = self.cleaned_data.get('text')
        rating = self.cleaned_data.get('rating')
        if rating and rating < 5 and len(text) < 50:
            raise forms.ValidationError('Text must be at least 50 characters for ratings less than 5.')
        return text