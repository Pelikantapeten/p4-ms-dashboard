"""
Views for app Dashboard
"""
from django.shortcuts import render
from django.views import generic
from dashboard.models import StudentMentorCard, StudentSession
from .forms import CreateSession


def start_page(request):
    """
    View for home page.
    """
    return render(request, 'index.html')


class MentorCard(generic.ListView):
    """
    View class for mentorcards
    """
    model = StudentMentorCard


class MentorCardDetails(generic.DetailView):
    """
    Detailed view class for mentorcards
    """
    model = StudentMentorCard


def session_list(request):
    """
    Sessions
    """
    sessions = StudentSession.objects.all()
    return render(request, 'sessions.html', {'sessions': sessions})


def session_detail(request, id):
    """
    Sessions details
    """
    id = StudentSession.objects.get(id=id)
    return render(request, 'session_detail.html', {'studentsession': id})