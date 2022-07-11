"""
Views for app Dashboard
"""
from django.shortcuts import render


def start_page(request):
    """
    View for home page.
    """
    return render(request, 'index.html')
