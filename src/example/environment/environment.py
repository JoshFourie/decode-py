from torch import nn
from torch.functional import Tensor

from ..policy.e_greedy import Policy

from typing import Any, Dict, Iterable
from typing_extensions import Protocol, runtime_checkable

from enum import Enum
from result import Result, Ok, Err

import gym

class Environment(Enum):
    '''
    Enum that lists all known environments.
    '''
    PONG = 0

@runtime_checkable
class StepHook(Protocol):
    '''
    Function that defines a hook applied after stepping an environment.
    '''
    def __call__(self, next_state: Any, reward: Any, done: bool, info: Any, **kwargs: Any) -> Result[Any, ValueError]: pass


class GymEnvironment:
    '''
    Class that manages an openai gym environment as a wrapper.
    '''

    env: Any
    policy: Policy

    ENVIRONMENTS: Dict[Environment, str] = {
        Environment.PONG : 'Pong-v0'
    }

    def __init__(self, environment: Environment) -> None:
        '''
        Makes an openai gym environment and inits the GymEnvironment wrapper.
        '''
        self.env = GymEnvironment.make(environment)

    @classmethod
    def make(cls, environment: Environment) -> Any: return gym.make(GymEnvironment.ENVIRONMENTS[environment])

    def actions_n(self) -> int: 
        '''
        Returns the number of actions in the action space.
        '''
        return self.env.action_space.n

    def action_space(self) -> Iterable[int]:
        '''
        Returns an iterator over the actions in the action space.
        '''
        actions_n = self.actions_n()
        return range(0, actions_n)

    def step(self, action: int, hook: StepHook, **kwargs: Any) -> Result[Any, ValueError]:
        '''
        Steps the environment and applies the hooks
        '''
        try:
            next_state, reward, done, info = self.env.step(action)
            output = hook(next_state, reward, done, info, **kwargs).expect('failed to run post step hook')
            return Ok(output)
        except ValueError as error: return Err(error)

    def set_policy(self, policy: Policy) -> Result[None, ValueError]:
        '''
        Sets a policy for the environment.
        '''
        self.policy = policy
        return Ok(None)

    def apply_policy(self, state: Tensor, net: nn.Module, **kwargs: Any) -> Result[int, ValueError]:
        '''
        Gets an action from the policy.
        '''
        try: getattr(self, 'policy')
        except ValueError as error: return Err(ValueError('policy has not been set', error))
        
        try:
            action: int = self.policy.sample(state, net, **kwargs).expect('tried to sample action with policy')
            return Ok(action)
        except ValueError as error: return Err(error)

    def reset(self) -> Result[Any, ValueError]:
        '''
        Resets an environment to the starting state.
        '''
        try: return Ok(self.env.reset())
        except ValueError as error: return Err(error)

    def render(self) -> Result[Any, ValueError]:
        '''
        Renders an environment on a local display port.
        '''
        try: return Ok(self.env.render())
        except ValueError as error: return Err(error)
        
    def close(self) -> Result[None, ValueError]:
        '''
        Closes and cleans up an environment.
        '''
        try:
            self.env.close()
            return Ok(None)
        except ValueError as error: return Err(error)
