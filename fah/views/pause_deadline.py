from django.shortcuts import render
from django.views import View
from matplotlib.figure import Figure

from fah.boinc import BoincSimulation
from fah.utils.utils import Utils


class PauseDeadline(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sim = BoincSimulation()

    def get(self, request):
        fig: Figure = self.sim.plot_pause_deadline()
        uri = Utils.get_image(fig=fig)
        return render(request=request, template_name='home.html', context={'data': uri})
