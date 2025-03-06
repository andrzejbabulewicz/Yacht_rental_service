from django import forms
from .models import Rental
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from datetime import date

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user
from django import forms
from .models import Rental

class RentalForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True, label="First Name")
    surname = forms.CharField(max_length=50, required=True, label="Last Name")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    skipper = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-group'})
    )
    life_jackets = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-group'})
    )
    gps = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-group'})
    )

    class Meta:
        model = Rental
        fields = ['start_date', 'end_date', 'name', 'surname', 'phone_number', 'skipper', 'life_jackets', 'gps']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be before the start date.")
            if start_date < date.today():
                raise forms.ValidationError("Start date cannot be in the past.")

        return cleaned_data
