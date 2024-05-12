from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                                             'placeholder': 'Логин'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True,
                                                                 'placeholder': 'Пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                                             'placeholder': 'Логин'}))
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control password-new', 'required': True,
                                           'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Повтор пароля",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control password-repeat', 'required': True,
                                           'placeholder': 'Повтор пароля'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'Эл. почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                            'placeholder': 'Эл. почта'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                                 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                                'placeholder': 'Фамилия'})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Данная эл. почта уже есть в системе!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                           'required': True,
                                                                                           'placeholder': 'Логин'}))
    email = forms.CharField(disabled=True, label="Эл. почта",
                            widget=forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                                          'placeholder': 'Эл. почта'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                                 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                                'placeholder': 'Фамилия'})
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                            'required': True,
                                                                                            'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(label="Новый пароль",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True,
                                                                      'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True,
                                                                      'placeholder': 'Подтверждение пароля'}))
