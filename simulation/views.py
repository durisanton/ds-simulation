import json
from typing import Union

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from matplotlib.figure import Figure

from simulation.boinc import BoincSimulation
from simulation.utils.utils import Utils

sim = BoincSimulation()
sim.make_net()


def plot_stats(request):
    fig: Figure = sim.plot_stats()
    uri = Utils.get_image(fig=fig)
    return render(request=request, template_name='home.html', context={'data': uri})


def plot_deadline(request):
    fig: Figure = sim.plot_deadline()
    uri = Utils.get_image(fig=fig)
    return render(request=request, template_name='home.html', context={'data': uri})


def plot_pause_deadline(request):
    fig = sim.plot_pause_deadline()
    uri = Utils.get_image(fig=fig)
    return render(request=request, template_name='home.html', context={'data': uri})


def plot_gant(request):
    fig = sim.plot_gant()
    uri = Utils.get_image(fig=fig)
    return render(request=request, template_name='home.html', context={'data': uri})


def params(request):
    return JsonResponse(model_to_dict(sim.params), safe=False, json_dumps_params={'indent': 2})


@csrf_exempt
def change_params(request):
    if request.method == "POST":
        data: dict[str: Union[int, list[int]]] = json.loads(request.body)
        sim.params.update(**data)
        return JsonResponse(data)
