from django.urls import path

from . import views

urlpatterns = [
    path("deadline", views.plot_deadline, name="deadline"),
    path("deadline/stats", views.plot_stats, name="deadline stats"),
    path("pause-deadline", views.plot_pause_deadline, name="pause deadline"),
    path("pause-deadline/stats", views.plot_stats, name="pause deadline stats"),
    path("gant", views.plot_gant, name="gant"),
    path("params", views.params, name="params"),
    path("change-params", views.change_params, name="change params")
]
