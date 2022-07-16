"""
Widgets for App Dashboard

Widgets:
FormsDatePicker - Creates date picker field for forms
"""
from django import forms


class FormsDatePicker(forms.DateInput):
    """
    Widget that will allow date picker in forms.
    Insipired by https://nancylin.xyz/
    """
    input_type = 'date'
