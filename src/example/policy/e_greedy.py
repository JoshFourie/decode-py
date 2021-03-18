from typing import Any, List
from result.result import Ok, Result
from typing_extensions import Protocol, runtime_checkable

from torch import Tensor, nn

import random

@runtime_checkable
class Policy(Protocol):
    '''
    Function signature that defines a policy.
    '''
    def sample(self, state: Tensor, net: nn.Module, **kwargs: Any) -> Result[int, ValueError]: pass

class eGreedy(Policy): 
    '''
    Class for the e-greedy policy algorithm.
    '''
    actions: List[int]

    def __init__(self, actions: int) -> None:
        '''
        Initialises an annealing epsilon-greedy policy class.
        '''
        self.actions = [action for action in range(actions)]

    def sample(self, state: Tensor, net: nn.Module, **kwargs: Any) -> Result[int, ValueError]:
        '''
        Samples actions given a state and deep learning network.
        '''
        preds: Tensor = net(state)
        weights: List[float] = list(preds.softmax(dim=0).view(-1))
        action: int = random.choices(self.actions, weights, k = 1).pop()
        return Ok(action)

