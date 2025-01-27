from django import forms
from .models import Client
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Housemaid

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email',  'field']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label="Search Clients")

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
    
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'passport', 'contact', 'contact2', 'medical', 'pcc',  'registration_status',  'designation',  'travel',  'interview', 'office', 'date_of_birth', 'age',  'comments']
        widgets = {
            'designation': forms.Select(choices=[
                ("", "Select Designation"),
                ("Cleaner", "Cleaner"),
                ("Security", "Security"),
                ("Helper", "Helper"),
                ("House Maid", "House Maid"),
                ("House to House", "House to House"),
                ("Beautician", "Beautician"),
                ("Technician", "Technician"),
                ("Hospitality", "Hospitality"),
                ("Barista", "Barista"),
                ("Caregiver", "Caregiver"),
                ("Driver", "Driver"),
                ("Hospital Helper", "Hospital Helper")
            ])
        }

    TRAVEL_CHOICES = [
        ('', 'Select'),  # Empty option
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    travel = forms.ChoiceField(choices=TRAVEL_CHOICES, widget=forms.Select(), required=False)

class HousemaidForm(forms.ModelForm):
    next_of_kin = forms.CharField(widget=forms.Textarea, required=False) 
    class Meta:
        model = Housemaid
        fields = '__all__'  # Include all fields from the model
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
    