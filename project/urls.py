"""URL routes for project."""

from django.urls import path

from . import views

app_name = "project"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("athletes/", views.AthleteListView.as_view(), name="athlete-list"),
    path(
        "athletes/<str:pk>",
        views.AthleteListView.as_view(),
        name="athlete-detail",
    ),
    path(
        "coaching-portal/",
        views.CoachPortalView.as_view(),
        name="coach-portal",
    ),
    path(
        "coaching-portal/programme/<str:pk>/",
        views.AthleteProgrammeSessionListView.as_view(),
        name="athlete-programme-session-list",
    ),
    path(
        "coaching-portal/programme/<str:pk>/create",
        views.AthleteProgrammeSessionCreateView.as_view(),
        name="athlete-programme-session-create",
    ),
    path(
        "coaching-portal/add-athlete/",
        views.AddAthleteView.as_view(),
        name="add-athlete",
    ),
    path(
        "coaching-portal/confirm-athlete/",
        views.ConfirmAthleteView.as_view(),
        name="confirm-athlete",
    ),
    path(
        "programme/",
        views.ProgrammeSessionListView.as_view(),
        name="programme-session-list",
    ),
    path(
        "programme/<str:pk>/",
        views.ProgrammeSessionDetailView.as_view(),
        name="programme-session-detail",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "profile/edit/", views.ProfileUpdateView.as_view(), name="profile-edit"
    ),
]
