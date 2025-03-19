from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text="Enter a strong password."
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        help_text="Enter the same password for confirmation."
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self) -> str:
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")

        # Optionally, validate password strength using Django's built-in validators
        validate_password(password1)

        return password2

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "To change the password, click <a href=\"../password/\">here</a>."
        )
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_active', 'is_staff')
