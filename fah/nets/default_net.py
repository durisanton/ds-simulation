from dataclasses import dataclass, field
from typing import List, Union

from petnetsim import PetriNet, Place, Transition, Arc, TransitionTimed, TransitionStochastic

from fah.models import Params


class DefaultNetException(Exception):
    pass


@dataclass
class DefaultNet:
    """
        default class for making petri nets
    """
    params: Params = field(default_factory=dataclass)
    places: List[Place] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    transitions: List[Union[Transition, TransitionTimed, TransitionStochastic]] = field(default_factory=list)

    def make_net(self) -> PetriNet:
        try:
            return PetriNet(self.places, self.transitions, self.arcs)
        except Exception:
            raise DefaultNetException(f'Base net creation error. \nCheck net params: {self.params.__dict__}')
