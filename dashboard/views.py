"""
Views for app Dashboard
"""
from django.shortcuts import render
from django.views import generic
#  from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from dashboard.models import StudentMentorCard, StudentSession
from .forms import CreateSession, EditSession


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


class SessionList(generic.ListView):
    """
    View class for list of sessions
    """
    model = StudentSession


class SessionDetalis(generic.DetailView):
    """
    Detailed view class for sessions
    """
    model = StudentSession


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


class UpdateSession(UpdateView):
    """
    View to updated existing sessions
    with student.
    """
    model = StudentSession
    template_name = 'sessionedit.html'
    form_class = EditSession
    success_url = '../sessions/'
