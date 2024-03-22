from django.shortcuts import render
from django.views import View

from fah.boinc import BoincSimulation
from fah.utils.utils import Utils


class Gant(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sim = BoincSimulation()

    def get(self, request):
        fig = self.sim.plot_gant()
        uri = Utils.get_image(fig=fig)
        return render(request=request, template_name='home.html', context={'data': uri})
