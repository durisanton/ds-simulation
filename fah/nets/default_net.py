from dataclasses import dataclass, field
from typing import List, Union

from petnetsim import PetriNet, Place, Transition, Arc, TransitionTimed, TransitionStochastic

from fah.models import Params


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
        return PetriNet(self.places, self.transitions, self.arcs)
