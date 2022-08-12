"""
Views for app Dashboard
"""
from django.shortcuts import render
from django.views import generic
from django.db.models import Sum
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


class SessionDeleteView(DeleteView):
    """
    View to delete existing student
    session
    """
    model = StudentSession
    success_url = '../sessions/'


def search_students(request):
    """
    function for search form in navbar
    inspired by:
    https://github.com/flatplanet/Django-Club-Youtube-Playlist
    """
    if request.method == "POST":
        searched = request.POST['searched']
        students = StudentMentorCard.objects.filter(
            mentor=request.user
            ).filter(
            student__name__icontains=searched,
        )
        return render(
            request,
            'search_students.html',
            {'searched': searched, 'students': students}
        )
    else:
        return render(
            request,
            'search_students.html',
            {}
        )


def time_report_view(request):
    """
    View for Time Report
    """
    # Calculates the total minutes and displays in format
    # (hours):(minutes)
    # Inspired by https://w3schools.com
    total_minutes = StudentSession.objects.filter(
        mentor=request.user
        ).aggregate(
            aggregate_total=Sum("time_spent")
        )["aggregate_total"]
    hours = total_minutes // 60
    minutes = total_minutes % 60
    hours_total = f"{hours}:{minutes}"
    
    context = {
        'hours_total': hours_total,
    }
    return render(
        request,
        'time-report.html',
        context
    )
