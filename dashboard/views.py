"""
Views for app Dashboard
"""
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
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


class StudentSessionView(CreateView):
    """
    View for the submitform for creating
    a student session.
    """
    model = StudentSession
    form_class = CreateSession
    template_name = 'sessionsubmit.html'
    success_url = '../sessions/'

    def form_valid(self, form):
        """
        Function that validates the user
        when using the form
        """
        form.instance.mentor = self.request.user
        return super(StudentSessionView, self).form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        """
        Function matching the query from
        CreateSession in forms and matches with
        current user.
        """
        kwargs = super(StudentSessionView, self).get_form_kwargs(
            *args, **kwargs
            )
        kwargs['user'] = self.request.user
        return kwargs
