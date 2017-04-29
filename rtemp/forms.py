from django import forms

class RoomCodeForm(forms.Form):
    room_code = forms.CharField(label='Enter your room code:', max_length=8)

    def clean_code(self):
        code = self.cleaned_data['code']
        return code
