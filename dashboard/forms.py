"""
Forms used by dashboard app
"""
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    Registration form for users with validation check on email
    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput
        )

    class Meta:
        """
        Meta class for fields
        """
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data
