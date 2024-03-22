import json
from typing import Union

from django.forms import model_to_dict
from django.http import JsonResponse
from django.views import View

from fah.boinc import BoincSimulation


class Params(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sim = BoincSimulation()

    def get(self, request):
        return JsonResponse(model_to_dict(self.sim.params), safe=False, json_dumps_params={'indent': 2})

    def post(self, request):
        data: dict[str: Union[int, list[int]]] = json.loads(request.body)
        self.sim.params.update(**data)
        return JsonResponse(data)
