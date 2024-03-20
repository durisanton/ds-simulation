from dataclasses import dataclass, field
from typing import List, Optional

from petnetsim import Transition, Place, Arc, PetriNet

from simulation.nets.default_net import DefaultNet
from simulation.nets.task_distribution_net import TaskDistributionNet


@dataclass
class BoincNet(DefaultNet):
    task_net: Optional[PetriNet] = None
    # place 'project' is a starting place for each task; place 'project_computed' is merging point for all task
    # results
    places: List[Place] = field(default_factory=lambda: [Place(name='project', init_tokens=1),
                                                         Place(name='project_computed')])
    transitions: List[Transition] = field(default_factory=lambda: [Transition('make_tasks'), Transition('merge_tasks')])
    arcs: List[Arc] = field(default_factory=lambda: [Arc(source='project', target='make_tasks'),
                                                     Arc(source='merge_tasks', target='project_computed')])

    def _make_task_net(self) -> None:
        self.task_net: PetriNet = TaskDistributionNet(params=self.params).make_net()

    def _clone_jobs(self) -> None:
        self._make_task_net()
        # cloning job tasks
        for task_i in range(1, self.params.tasks + 1):
            prefix: str = self._make_prefix(task_id=task_i)
            self.task_net.clone(prefix, self.places, self.transitions, self.arcs)
            self.places.append(Place(f'task{task_i}'))
            self.arcs.append(Arc(source=f'task{task_i}', target=f'{prefix}distribution'))
            self.arcs.append(Arc(source='make_tasks', target=f'task{task_i}'))
            self.arcs.append(Arc(source=f'{prefix}results', target='merge_tasks', n_tokens=self.params.compare_results))

    def make_net(self) -> PetriNet:
        self._clone_jobs()
        return PetriNet(self.places, self.transitions, self.arcs)

    @staticmethod
    def _make_prefix(task_id) -> str:
        return f'task{str(task_id)}_'
