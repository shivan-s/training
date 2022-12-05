"""URL routes for project."""

from django.urls import path

from . import views

app_name = "project"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "portal/",
        views.CoachPortalView.as_view(),
        name="coach-portal",
    ),
    path("athletes/", views.AthleteListView.as_view(), name="athlete-list"),
    path(
        "portal/athletes/<str:pk>/programme/list",
        views.CoachProgrammeSessionListView.as_view(),
        name="coach-programme-session-list",
    ),
    path(
        "hx/portal/athletes/<str:athlete_pk>/programme/<str:pk>",
        views.hx_coach_programme_session_update_view,
        name="hx-coach-programme-session-update",
    ),
    path(
        "hx/portal/athletes/<str:athlete_pk>/programme/",
        views.hx_coach_programme_session_update_view,
        name="hx-coach-programme-session-new",
    ),
    path(
        "hx/portal/athletes/<str:pk>/programme-new-week/",
        views.hx_coach_programme_session_week_duplicate_view,
        name="hx-coach-programme-session-week-duplicate",
    ),
    path(
        "hx/portal/athletes/<str:athlete_pk>/programme/<str:programme_session_pk>/exercise/<str:pk>",
        views.hx_coach_exercise_update_view,
        name="hx-coach-exercise-update",
    ),
    path(
        "hx/portal/athletes/<str:athlete_pk>/programme/<str:programme_session_pk>/exercise/",
        views.hx_coach_exercise_update_view,
        name="hx-coach-exercise-new",
    ),
    path(
        "hx/portal/athletes/<str:athlete_pk>/programme/<str:programme_session_pk>/exercise/<str:exercise_pk>/exercise_set/<str:pk>",
        views.hx_coach_exercise_set_update_view,
        name="hx-coach-exercise-set-update",
    ),
    path(
        "hx/portal/athletes/<str:athlete_pk>/programme/<str:programme_session_pk>/exercise/<str:exercise_pk>/exercise_set/",
        views.hx_coach_exercise_set_update_view,
        name="hx-coach-exercise-set-new",
    ),
    path(
        "portal/add-athlete/",
        views.AddAthleteView.as_view(),
        name="add-athlete",
    ),
    path(
        "portal/confirm-athlete/",
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
    path(
        "library/",
        views.ExerciseTypeListView.as_view(),
        name="exercise-type-list",
    ),
    path(
        "library/<str:pk>/",
        views.ExerciseTypeDetailView.as_view(),
        name="exercise-type-detail",
    ),
]
