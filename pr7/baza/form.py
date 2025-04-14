from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from django.http import HttpRequest
from django.contrib.auth.models import User
from account1.models import Profile, Gender
from order.models import Order
from datetime import date, timedelta



 
class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(  
            attrs={
                'autocomplete': 'text',
                'placeholder': 'введите логин',
                'class': 'input',
            }
        ),
        required=False,
        validators=[RegexValidator(r'[0-9а-яА-ЯёЁ]', "Введите логин кириллицей")],
        label=''
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
                'placeholder': 'Введите эл. почту',
                'class': 'input'
                
                
            }
        ),
        required=False,
        label=''
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Введите пароль',
                'class': 'input',
                
            }
        ),
        required=False,
        label=''
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторите пароль',
                'class': 'input',
                
            }
        ),
        required=False,
        label=''
    )

        
    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            raise forms.ValidationError('Введите эл. почту', code='invalid')
        return email
        
    def clean_password1(self):
        password = self.cleaned_data['password1']
        if password == '':
            raise forms.ValidationError('Введите пароль', code='invalid')
        return password
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if username == '':
            raise forms.ValidationError('Введите логин', code='invalid')
        return username
        
        
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "password1", "password2")
        
class Login_Form(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'text',
                'placeholder': 'Логин',
                'class': 'input',
            }
        ),
        required=False,
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': 'Пароль',
                'class': 'input',
            }
        ),
        required=True,
        label=''
    )
    
    error_messages = {
        "invalid_login": (
            "неверный логин или пароль"
        ),
    }

    
    def cleab_password(self):
        password = self.cleaned_data['password']
        if password == '':
            raise forms.ValidationError('Введите пароль', code='invalid')
        return password
    
    def cleab_username(self):
        username = self.cleaned_data['username']
        if username == '':
            raise forms.ValidationError('Введите логин', code='invalid')
        if not User.objects.filter(username=username):
            raise forms.ValidationError('Пользователя не существует', code='invalid')
        return username
        
        
from account1.models import Profile
from account1.models import Avatar
class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['gender', 'country', 'city', 'street', 'house', 'apartament_number', 'avatar']
        widgets = {
            'gender': forms.Select(choices=Gender.choices),
            'country': forms.TextInput(attrs={'placeholder': 'Страна'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город'}),
            'street': forms.TextInput(attrs={'placeholder': 'Улица'}),
            'house': forms.TextInput(attrs={'placeholder': 'Дом'}),
            'apartament_number': forms.TextInput(attrs={'placeholder': 'Номер квартиры'}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            if self.cleaned_data['avatar']:
                Avatar.objects.update_or_create(user=profile.user, defaults={'avatar': self.cleaned_data['avatar']})
        return profile
                


class OrderForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': (date.today() + timedelta(days=10)).isoformat() 
            }
        ),
        label="Дата начала"
    )

    class Meta:
        model = Order
        fields = ['customer_email', 'start_date']
        
        
        
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'textarea-1'}),
            
        }


