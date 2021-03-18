'''
This module implements abstract classes for blocks related to observations for agent learning with PyTorch.
'''

from typing import Any, Generic, TypeVar

from result import Result, Ok, Err
from ...interface.observation import Observation, ObservationFactory


S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

class OpenAI_Observation(Generic[S, T, U, V], Observation[S, T, U, V]):
    '''
    Subclass of ABC Observation for OpenAI gym environments.

    Generics:
        S : some type representing a state
        T ; some type reprsenting a reward
        U : some type representing a transition
        V : some type representing an action
    '''

    state: S
    reward: T
    transition: U
    action: V

    def __init__(self, state: S, reward: T, transition: U, action: V, **kwargs: Any) -> None:
        '''
        Sets the values for state, reward, transition and action.
        '''
        self.state = state
        self.reward = reward
        self.transition = transition
        self.action = action

    def set_reward_(self, reward: T) -> Result[None, ValueError]: 
        '''
        Sets the reward to this value.
        '''
        try:
            self.reward = reward
            return Ok(None)
        except ValueError as error: return Err(ValueError(error))


    def get_reward(self, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Returns a reward stored in this observation.
        '''
        try: return Ok(self.reward)

        except ValueError as error: return Err(ValueError(error))

    def set_state_(self, state: S) -> Result[None, ValueError]:
        '''
        Sets the state for this obervation.
        '''
        try:
            self.state = state
            return Ok(None)
        except ValueError as error: return Err(ValueError(error))

    def get_state(self, **kwargs: Any) -> Result[S, ValueError]:
        '''
        Returns a state stored in this observation.
        '''
        try: return Ok(self.state)

        except ValueError as error: return Err(ValueError(error))

    def set_next_state_(self, next_state: U) -> Result[None, ValueError]:
        '''
        Sets the next_state for this obervation.
        '''
        try:
            self.transition = next_state
            return Ok(None)
        except ValueError as error: return Err(ValueError(error))

    def get_next_state(self, **kwargs: Any) -> Result[U, ValueError]:
        '''
        Returns a next_state stored in this observation.
        '''
        try: return Ok(self.transition)

        except ValueError as error: return Err(ValueError(error))

    def set_action_(self, action: V) -> Result[None, ValueError]:
        '''
        Sets the next_state for this obervation.
        '''
        try:
            self.action = action
            return Ok(None)
        except ValueError as error: return Err(ValueError(error))

    def get_action(self, **kwargs: Any) -> Result[V, ValueError]:
        '''
        Returns an action stored in this observation.
        '''
        try: return Ok(self.action)

        except ValueError as error: return Err(ValueError(error))


ObservationFactoryType = ObservationFactory[S, T, U, V, OpenAI_Observation[S, T, U, V]]

class OpenAI_ObservationFactory(Generic[S, T, U, V], ObservationFactoryType[S, T, U, V]):
    '''
    Factory for creating instances of OpenAI_Observations.
    '''

    @classmethod
    def new(cls, state: S, reward: T, transition: U, action: V) -> Result[OpenAI_Observation[S, T, U, V], ValueError]:
        '''
        Creates a new instance of an OpenAI_Observation.
        '''
        try:
            return Ok(OpenAI_Observation(
                state = state,
                reward = reward,
                transition = transition,
                action = action
            ))
        except Exception as error: return Err(ValueError(error, 'failed to create OpenAI_Observation instance.'))
