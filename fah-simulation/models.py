import json

from django.contrib.postgres.fields import ArrayField
from django.db.models import IntegerField, Model


class Params(Model):
    tasks = IntegerField(default=0)
    clients = IntegerField(default=0)
    loops = IntegerField(default=0)
    max_steps = IntegerField(default=0)
    compare_results = IntegerField(default=0)
    stats_loops = IntegerField(default=0)
    # probability and times of transitions for individual clients
    connect_min_time = ArrayField(IntegerField(), default=list, blank=True)
    connect_max_time = ArrayField(IntegerField(), default=list, blank=True)
    pc_initialization_min_time = ArrayField(IntegerField(), default=list, blank=True)
    pc_initialization_max_time = ArrayField(IntegerField(), default=list, blank=True)
    client_running_probability = ArrayField(IntegerField(), default=list, blank=True)
    client_crash_probability = ArrayField(IntegerField(), default=list, blank=True)
    compute_1_min_time = ArrayField(IntegerField(), default=list, blank=True)
    compute_1_max_time = ArrayField(IntegerField(), default=list, blank=True)
    pause_on_probability = ArrayField(IntegerField(), default=list, blank=True)
    pause_off_probability = ArrayField(IntegerField(), default=list, blank=True)
    in_pause_min_time = ArrayField(IntegerField(), default=list, blank=True)
    in_pause_max_time = ArrayField(IntegerField(), default=list, blank=True)
    job_running_probability = ArrayField(IntegerField(), default=list, blank=True)
    job_crash_probability = ArrayField(IntegerField(), default=list, blank=True)
    compute_2_min_time = ArrayField(IntegerField(), default=list, blank=True)
    compute_2_max_time = ArrayField(IntegerField(), default=list, blank=True)
    correct_probability = ArrayField(IntegerField(), default=list, blank=True)
    incorrect_probability = ArrayField(IntegerField(), default=list, blank=True)

    def update(self, **kwargs):
        for name, values in kwargs.items():
            try:
                setattr(self, name, values)
            except KeyError:
                pass
        self.save()

    @staticmethod
    def load_params() -> dict:
        with open(file='fah-simulation/fixtures/params.json') as file:
            params_dict = json.load(file)
        return params_dict

    @classmethod
    def init(cls):
        if Params.objects.first() is None:
            Params(**cls.load_params()).save()
        return Params.objects.first()
