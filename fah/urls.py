from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from fah.views import plot_stats, plot_deadline, plot_pause_deadline, plot_gant, params, change_params

urlpatterns = [
    path("deadline", plot_stats, name="deadline"),
    path("deadline/stats", plot_deadline, name="deadline stats"),
    path("pause-deadline", plot_pause_deadline, name="pause deadline"),
    path("pause-deadline/stats", plot_stats, name="pause deadline stats"),
    path("gant", plot_gant, name="gant"),
    path("params", params, name="params"),
    path("change-params", csrf_exempt(change_params), name="change params")
]
