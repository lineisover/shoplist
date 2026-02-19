from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повтор пароля')

    class Meta:
        model = User
        fields = ("email", "nick_name")
        labels = {
            "email": "Электронная почта",
            "nick_name": "Никнейм",
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

        validate_password(password2)
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            email=self.cleaned_data["email"],
            nick_name=self.cleaned_data["nick_name"],
            password=self.cleaned_data["password1"],
        )
        return user
