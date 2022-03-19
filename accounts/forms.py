from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, CharField
from django.contrib.auth.forms import UserCreationForm
from .models import UserModel


class CreateUserForm(UserCreationForm):
    password1 = CharField(
        label="Password",
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        ),
    )
    password2 = CharField(
        label="Confirm password",
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Repeat Password'
            }
        ),
    )

    class Meta:
        model = UserModel
        fields = [
            'username',
            # 'first_name',
            # 'last_name',
            # 'email',
            'password1',
            'password2'
        ]
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Username'
            }),

            # 'first_name': TextInput(attrs={
            #     'class': "form-control",
            #     'style': 'max-width: 300px;',
            #     'placeholder': 'First Name'
            # }),
            #
            # 'last_name': TextInput(attrs={
            #     'class': "form-control",
            #     'style': 'max-width: 300px;',
            #     'placeholder': 'Last Name'
            # }),
            # 'email': EmailInput(attrs={
            #     'class': "form-control",
            #     'style': 'max-width: 300px;',
            #     'placeholder': 'Email'
            # })
        }
