from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']

    # Сделаем поле пароля необязательным
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "password"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if len(phone_number) < 11 or len(phone_number) > 14:
            raise ValidationError("Номер телефона должен быть от 11 до 14 символов.")
        if not phone_number.startswith("+"):
            raise ValidationError("Номер телефона должен начинаться с +.")
        if not phone_number[1:].isdigit():
            raise ValidationError("Номер телефона должен состоять только из цифр.")
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Пользователь с таким номером телефона уже существует.")
        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Пароль должен быть не менее 8 символов.")
        return password

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email
