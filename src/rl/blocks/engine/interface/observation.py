'''
This module adds abstract classes for blocks related to observations for agent learning.
'''

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from result import Result, Err


S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

class Observation(ABC, Generic[S, T, U, V]):
    '''
    ABC for managing observations in an environment.

    Based on needs for model-free learning.

    Generics:
        S : some state in an environment.
        T : some reward in an environment.
        U : some transition or future state in an environment.
        V : some action in an environment.
    '''

    @abstractmethod
    def set_reward_(self, reward: T) -> Result[None, ValueError]:
        '''
        Sets the reward for this obervation.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def get_reward(self, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Returns a reward stored in this observation.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def set_state_(self, state: S) -> Result[None, ValueError]:
        '''
        Sets the state for this obervation.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def get_state(self, **kwargs: Any) -> Result[S, ValueError]:
        '''
        Returns a state stored in this observation.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def get_next_state(self, **kwargs: Any) -> Result[U, ValueError]:
        '''
        Returns a next_state stored in this observation.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def set_next_state_(self, next_state: U) -> Result[None, ValueError]:
        '''
        Sets the next_state for this obervation.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def set_action_(self, action: V) -> Result[None, ValueError]:
        '''
        Sets the next_state for this obervation.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def get_action(self, **kwargs: Any) -> Result[V, ValueError]:
        '''
        Returns an action stored in this observation.
        '''
        return Err(ValueError(NotImplementedError))


X = TypeVar('X')
class ObservationFactory(ABC, Generic[S, T, U, V, X]):
    '''
    Factory for creating instances of Observation classes.

    Generics:
        S : some type representing a state
        T : some type representing a reward
        U : some type representing a transition
        V : some type representing an action
        X : some type to be created by the factory
    '''

    @abstractmethod
    def new(cls, state: S, reward: T, transition: U, action: V) -> Result[X, ValueError]:
        '''
        Creates an instance of type X.
        '''
        return Err(ValueError(NotImplementedError))
        