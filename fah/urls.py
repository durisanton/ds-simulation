from django.urls import path

from fah.views.deadline import Deadline
from fah.views.gant import Gant
from fah.views.params import Params
from fah.views.pause_deadline import PauseDeadline
from fah.views.stats import Stats

urlpatterns = [
    path("deadline", Deadline.as_view(), name="deadline"),
    path("deadline/stats", Stats.as_view(), name="deadline stats"),
    path("pause-deadline", PauseDeadline.as_view(), name="pause deadline"),
    path("pause-deadline/stats", Stats.as_view(), name="pause deadline stats"),
    path("gant", Gant.as_view(), name="gant"),
    path("params", Params.as_view(), name="params"),
    path("change-params", Params.as_view(), name="change params")
]
