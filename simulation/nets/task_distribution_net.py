from dataclasses import dataclass, field
from typing import List

from petnetsim import PetriNet, Place, Transition, Arc

from simulation.utils.constants import Constants
from simulation.nets.default_net import DefaultNet


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
                if tr.name == 'connect':
                    tr.t_min = self.params.connect_min_time[client_i - 1]
                    tr.t_max = self.params.connect_max_time[client_i - 1]
                if tr.name == 'pc_initialization':
                    tr.t_min = self.params.pc_initialization_min_time[client_i - 1]
                    tr.t_max = self.params.pc_initialization_max_time[client_i - 1]
                if tr.name == 'client_running':
                    tr.probability = self.params.client_running_probability[client_i - 1]
                if tr.name == 'client_crash':
                    tr.probability = self.params.client_crash_probability[client_i - 1]
                if tr.name == 'compute_1':
                    tr.t_min = self.params.compute_1_min_time[client_i - 1]
                    tr.t_max = self.params.compute_1_max_time[client_i - 1]
                if tr.name == 'pause_off':
                    tr.probability = self.params.pause_off_probability[client_i - 1]
                if tr.name == 'pause_on':
                    tr.probability = self.params.pause_on_probability[client_i - 1]
                if tr.name == 'in_pause':
                    tr.t_min = self.params.in_pause_min_time[client_i - 1]
                    tr.t_max = self.params.in_pause_max_time[client_i - 1]
                if tr.name == 'job_running':
                    tr.probability = self.params.job_running_probability[client_i - 1]
                if tr.name == 'job_crash':
                    tr.probability = self.params.job_crash_probability[client_i - 1]
                if tr.name == 'compute_2':
                    tr.t_min = self.params.compute_2_min_time[client_i - 1]
                    tr.t_max = self.params.compute_2_max_time[client_i - 1]
                if tr.name == 'correct':
                    tr.probability = self.params.correct_probability[client_i - 1]
                if tr.name == 'incorrect':
                    tr.probability = self.params.incorrect_probability[client_i - 1]

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
