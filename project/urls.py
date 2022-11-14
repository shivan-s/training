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
        "coaching_portal/",
        views.CoachPortalView.as_view(),
        name="coach-portal",
    ),
    path(
        "your_training/",
        views.YourTraining.as_view(),
        )
    path("athlete_add/", views.AthleteAddView.as_view(), name="athlete-add"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "profile/edit/", views.ProfileUpdateView.as_view(), name="profile-edit"
    ),
]
