from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(max_length=48, min_length=4, label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nome do usuario'}))

    password = forms.CharField(max_length=16, min_length=8, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Senha'}
    ))

    pwd_db = forms.CharField(max_length=16, min_length=4, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Senha do DataBase'}
    ))


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='', min_length=5, max_length=48, widget=forms.TextInput(attrs={
            'placeholder': 'Nome do usuario',
        }
    ))

    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
        }
    ))

    password1 = forms.CharField(min_length=8, label='password', widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha',
        }
    ))
    password2 = forms.CharField(min_length=8, label='Confirm password', widget=forms.PasswordInput(attrs={
            'placeholder': 'Comfirme a senha',
        }
    ))
    pwd_db = forms.CharField(min_length=4, label='Confirm password', widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha do DataBase',
        }
    ))

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        try:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']

            if not password1 or not password2 or password1 != password2:
                raise ValidationError("Password don't match")
            else:
                return password2
        except KeyError:
            return ValidationError("both fields need to be filled")

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class EditUserForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email

    class Meta:
        model = User
        fields = ["username", "email"]

    username = forms.CharField(label='username', min_length=5, max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Nome do usuario'}
    ))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={
        'placeholder': 'Email'}
    ))
    password1 = forms.CharField(required=False, label='password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha'}
    ))
    password2 = forms.CharField(required=False, label='Confirm password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Comfirme a senha'}
    ))

    pwd_db = forms.CharField(required=False, label='DataBase password', widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha do DataBase'}))

    def username_clean(self, data, user):
        name = user.username
        newname = data['username']
        new = User.objects.filter(username=newname)
        if not new.count() or name == newname:
            return newname
        else:
            raise ValidationError('Username ja existe')

    def email_clean(self, data, user):
        newemail = data['email']
        email = user.email
        new = User.objects.filter(email=newemail)
        if not new.count() or email == newemail:
            return newemail
        else:
            raise ValidationError('Email ja usado por outra conta')

    def password_clean(self, data):
        pwd1 = data['password1']
        pwd2 = data['password2']
        if pwd1 == pwd2 and len(pwd1) >= 8 or pwd1 == '':
            return pwd1
        else:
            raise ValidationError('As senhas precisam ser iguais')

    def is_valid(self, user, data):
        if self.username_clean(data, user):
            return True
        if self.email_clean(data, user):
            return True
        if self.password_clean(data):
            return True
