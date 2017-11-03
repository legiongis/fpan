from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Scout, ScoutProfile


class ScoutForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={'class':'form-control'}))
    middle_initial = forms.CharField(
        max_length=2,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label="Enter Password")    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label="Re-enter Password")
    class Meta:
        model = Scout
        fields = ('first_name', 'middle_initial', 'last_name', 'email', 'password1', 'password2')


class ScoutProfileForm(forms.ModelForm):
    class Meta:
        model = ScoutProfile
        fields = ('street_address', 'city', 'state', 'zip_code', 'phone', 'background', 'relevant_experience', 'interest_reason', 'site_interest_type', 'region_choices', 'ethics_agreement')
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'background': forms.Textarea(attrs={'class': 'form-control'}),
            'relevant_experience': forms.Textarea(attrs={'class': 'form-control'}),
            'interest_reason': forms.Textarea(attrs={'class': 'form-control'}),
            'site_interest_type': forms.Select(attrs={'class': 'form-control'}),
            'region_choices': forms.CheckboxSelectMultiple(),
            'ethics_agreement': forms.CheckboxInput(),
        }