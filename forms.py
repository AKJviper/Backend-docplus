from django.forms import ModelForm
from django.forms.forms import Form
from .models import UserDoctor , AppUser
from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username = forms.CharField(max_length=50 , required=True, widget=forms.TextInput(attrs={'class':'username', 'placeholder':'Enter your username or Email'}),label="Username")
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'class':'inpBx', 'placeholder':'Enter your password'}),label="password")
    remember = forms.CheckboxInput()


class RegisterForm(ModelForm):
     
        def __init__(self, *args, **kwargs):
            super(RegisterForm, self).__init__(*args, **kwargs)
            self.fields['dob'].widget.attrs={'type':'text', 'class':'input','id':'datepicker' }
            self.fields['city'].widget.attrs={'placeholder':'Enter your city', 'class':'input','id':'cityList' }
            self.fields['state'].widget.attrs={'class':'input','id':'stateList' }
            self.fields['address_line'].widget.attrs={'placeholder':'Address', 'class':'input','id':'address' }
            # self.fields['state'].widget.attrs={'placeholder':'Enter your state','id':'stateList' }

        class Meta:
            model = AppUser
            fields = '__all__'
            exclude = ('userin',)
            labels = {
                "address_line" : 'Address or Area'
            }
class DoctorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['desc'].widget.attrs={'type':'text', 'placeholder':'Degree and Specialiasation','class':'input','id':'doctor_desc' }   
        self.fields['apnt_fees'].widget.attrs={'type':'text','class':'input','id':'apnt_fees' }   
        self.fields['consult_fees'].widget.attrs={'type':'text', 'placeholder':'Online Consult Fees','class':'input','id':'consult_fees' }        
        self.fields['availability'].widget.attrs={'type':'boolean', 'placeholder':'From','class':'input','id':'available' }   

    class Meta:
            model = UserDoctor
            exclude = ('Doctor_Name', 'Time_from', 'Time_to','userdoc',)
            labels = {
                "Time_from" : 'From',
                "Time_to" : 'to'
            }
            widgets = {
            'Time_from': forms.TimeInput(format='%H:%M'),
        }
        

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class': 'inputBx', 'placeholder': 'First Name'}), label="First Name")
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', widget=forms.TextInput(attrs={'class': 'inputBx', 'placeholder': 'Last Name'}), label="Last Name")
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'class': 'inputBx', 'placeholder': 'Email'}), label="Email")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )


    


# username_validator = UnicodeUsernameValidator()

# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: First Name', widget=forms.TextInput(attrs={'class': 'inputBx', 'placeholder': 'First Name'}), label="first_name")
#     last_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: Last Name', widget=forms.TextInput(attrs={'class': 'inputBx', 'placeholder': 'Last Name'}), label="last_name")
#     email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.',        widget=forms.TextInput(attrs={'class': 'inputBx', 'placeholder': 'Email'}), label="email")
#     password1 = forms.CharField(label=('Password'),
#                                 widget=(forms.PasswordInput(attrs={'class': 'inputBx', 'placeholder': 'Password', 'autocomplete':'off'})),
#                                 help_text=password_validation.password_validators_help_text_html())
#     password2 = forms.CharField(label=('Password confirmation'), widget=forms.PasswordInput(attrs={'class': 'inputBx', 'placeholder': 'Confirm Password', 'autocomplete':"new-password"}),
#                                 help_text=('Enter the same password, for confirmation'))
#     username = forms.CharField(
#         label=('Username'),
#         max_length=150,
#         help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[username_validator],
#         error_messages={'unique': ("A user with that username already exists.")},
#         widget=forms.TextInput(attrs={'class': 'inputBx', 'placeholder': 'Username'})
#     )

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
    
#     def save(self, commit=True):
#         user = super(SignUpForm, self).save()
#         user.email = self.cleaned_data["email"]
#         user.first_name = self.cleaned_data["first_name"]
#         user.last_name = self.cleaned_data["last_name"]
#         user.username = self.cleaned_data["username"]
#         user.password1 = self.cleaned_data["password1"]
#         user.password2 = self.cleaned_data["password2"]
#         user.save()
#         return user

