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


def session_form_view(request):
    """
    View for create Student Session page
    Created this by looking at the view created by CluelessBiker,
    in her project:
    https://github.com/CluelessBiker/project4-print-statements
    """
    if request.method == 'POST':
        create_session_form = CreateSession(request.POST, request.FILES)
        if create_session_form.is_valid():
            create_session_form.instance.mentor = request.user
            create_session_form.save()
            messages.success(
                request, "You have created a new session")
            return redirect('session-list')
        else:
            create_session_form = CreateSession()

    return render(
        request,
        'sessionsubmit.html',
        {
            'create_session_form': CreateSession(),
        },
    )
