"""
Forms used by dashboard app
"""
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import StudentSession, StudentMentorCard, MentorNotes
from .widget import FormsDatePicker

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


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating admin users. Includes all the required
    fields, plus a repeated password.
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        """
        Meta class for fields
        """
        model = User
        fields = ['email', 'password', 'is_active', 'admin', 'staff', 'name']

    def clean_password(self):
        """
        Returns the intitial valure of the input from the user
        """
        return self.initial["password"]


class CreateSession(forms.ModelForm):
    """
    Form for creating a student/mentor session
    """
    class Meta:
        """
        Generate which fields should be displayed.
        """
        model = StudentSession
        fields = (
            'StudentMentorCard',
            'project_link',
            'project_repo',
            'summary',
            'session_date',
            'time_spent',
            'type',
            'subject',
        )
        labels = {
            'StudentMentorCard': 'Student',
            'project_link': 'Project URL',
            'project_repo': 'Project repository',
            'summary': 'Write a summary of the session',
            'session_date': 'Choose date of the session',
            'time_spent': 'Choose lenght of the session',
            'type': 'Choose type of session',
            'subject': 'Choose subject of session',
        }
        widgets = {
            'session_date': FormsDatePicker,
        }
        help_texts = {
            'summary': None,
            'time_spent': None,
            'type': None,
            'subject': None,
        }

    def __init__(self, *args, **kwargs):
        """
        Function that returns the Students
        that belong to a specific mentor to the
        selection of students in the form. Created
        by searching for information on https://stackoverflow.com/
        """
        user = kwargs.pop('user', None)
        super(CreateSession, self).__init__(*args, **kwargs)
        if user:
            studentmentorcard = StudentMentorCard.objects.filter(
                Q(mentor=user) | Q(mentor=user)
                )
            self.fields['StudentMentorCard'].queryset = studentmentorcard


class EditSession(forms.ModelForm):
    """
    Form for editing a student/mentor session
    """
    class Meta:
        """
        Generate which fields should be displayed.
        """
        model = StudentSession
        fields = (
            'project_link',
            'project_repo',
            'summary',
            'session_date',
            'time_spent',
            'type',
            'subject',
        )
        labels = {
            'project_link': 'Project URL',
            'project_repo': 'Project repository',
            'summary': 'Write a summary of the session',
            'session_date': 'Choose date of the session',
            'time_spent': 'Choose lenght of the session',
            'type': 'Choose type of session',
            'subject': 'Choose subject of session',
        }
        widgets = {
            'session_date': FormsDatePicker,
        }
        help_texts = {
            'summary': None,
            'time_spent': None,
            'type': None,
            'subject': None,
        }


class CreateNote(forms.ModelForm):
    """
    Form for creating a note on a student
    """
    class Meta:
        """
        Generate which fields should be displayed.
        """
        model = MentorNotes
        fields = (
            'student_card',
            'mentor_note',
        )
        labels = {
            'mentor_note': 'Note',
        }

        help_texts = {

        }

    def __init__(self, *args, **kwargs):
        """
        Function that returns the Students
        that belong to a specific mentor to the
        selection of students in the form. Created
        by searching for information on https://stackoverflow.com/
        """
        user = kwargs.pop('user', None)
        super(CreateNote, self).__init__(*args, **kwargs)
        if user:
            student_card = StudentMentorCard.objects.filter(
                Q(mentor=user) | Q(mentor=user)
                )
            self.fields['student_card'].queryset = student_card
