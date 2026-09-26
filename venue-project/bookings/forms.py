from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["date", "start_time", "end_time", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "input"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "input"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "input"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "input", "placeholder": "Anything the host should know?"}),
        }
