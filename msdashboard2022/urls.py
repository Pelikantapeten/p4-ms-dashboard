"""msdashboard2022 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.start_page, name='home'),
    path('mentorcards/', views.MentorCard.as_view(
        template_name='mentorcards.html'),
        name='mentorcards'
        ),
    path('mentorcards/<int:pk>', views.MentorCardDetails.as_view(
        template_name='mentorcard_detail.html'),
        name='student-mentor-card'
        ),
    path('sessions/', views.SessionList.as_view(
        template_name='sessions.html'),
        name='student-sessions'
    ),
    path('sessions/<int:pk>/', views.SessionDetalis.as_view(
        template_name='session_detail.html'),
        name='student-session'
    ),
    path(
        'sessionsubmit/',
        views.StudentSessionView.as_view(),
        name='sessionsubmit'
    ),
    path(
        'sessionupdate/<int:pk>',
        views.UpdateSession.as_view(),
        name='sessionedit'
    ),
    path(
        'delete/<pk>',
        views.SessionDeleteView.as_view(template_name="confirm_delete.html"),
        name='delete-session'
    ),
    path(
        'search_students',
        views.search_students,
        name="search_students"
    )
]
