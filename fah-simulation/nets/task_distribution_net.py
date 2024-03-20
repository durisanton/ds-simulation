from dataclasses import dataclass, field
from typing import List, Union

from petnetsim import PetriNet, Place, Transition, Arc, TransitionStochastic, TransitionTimed

from simulation.nets.default_net import DefaultNet
from simulation.utils.constants import Constants


@dataclass
class TaskDistributionNet(DefaultNet):
    """
        some stuff for cloning client nets; transition 'task_distribution' is a starting place for all cloned nets;
        place 'results' is merging point for all client results
    """
    client_net: PetriNet = DefaultNet(places=Constants.places, arcs=Constants.input_arcs+Constants.output_arcs,
                                      transitions=Constants.transitions).make_net()
    places: List[Place] = field(default_factory=lambda: [Place('results'), Place('results_counter')])
    transitions: List[Transition] = field(default_factory=lambda: [Transition('distribution')])

    # cloning clients
    def _clone_clients(self) -> None:
        for client_i in range(1, self.params.clients + 1):
            # filling probability and time data to transitions
            for tr in self.client_net.transitions:
                if isinstance(tr, TransitionTimed):
                    tr_to_params_mapping: Union[tuple[list], tuple[list, list]] = self._get_mapping(
                        tr_name=tr.name)
                    tr.t_min = tr_to_params_mapping[0][client_i - 1]
                    tr.t_max = tr_to_params_mapping[1][client_i - 1]
                elif isinstance(tr, TransitionStochastic):
                    tr_to_params_mapping: Union[tuple[list], tuple[list, list]] = self._get_mapping(
                        tr_name=tr.name)
                    tr.probability = tr_to_params_mapping[0][client_i - 1]

            prefix: str = self._make_prefix(client_id=client_i)

            self.client_net.clone(prefix, self.places, self.transitions, self.arcs)
            self.arcs.append(Arc(source='distribution', target=f'{prefix}waiting'))
            self.arcs.append(Arc(source=f'{prefix}merge', target='results'))
            self.arcs.append(Arc(source=f'{prefix}merge', target='results_counter'))

    def make_net(self) -> PetriNet:
        self._clone_clients()
        return PetriNet(self.places, self.transitions, self.arcs)

    @staticmethod
    def _make_prefix(client_id: int) -> str:
        return f'client{str(client_id)}_'

    def _get_mapping(self, tr_name: str) -> Union[tuple[list], tuple[list, list]]:
        return {
            'connect': (self.params.connect_min_time, self.params.connect_max_time),
            'pc_initialization': (self.params.pc_initialization_min_time, self.params.pc_initialization_max_time),
            'client_running': (self.params.client_running_probability,),
            'client_crash': (self.params.client_crash_probability,),
            'compute_1': (self.params.compute_1_min_time, self.params.compute_1_max_time),
            'pause_off': (self.params.pause_off_probability,),
            'pause_on': (self.params.pause_on_probability,),
            'in_pause': (self.params.in_pause_min_time, self.params.in_pause_max_time),
            'job_running': (self.params.job_running_probability,),
            'job_crash': (self.params.job_crash_probability,),
            'compute_2': (self.params.compute_2_min_time, self.params.compute_2_max_time),
            'correct': (self.params.correct_probability,),
            'incorrect': (self.params.incorrect_probability,),
        }[tr_name]
