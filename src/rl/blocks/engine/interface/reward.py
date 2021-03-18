'''
This module adds abstract classes for blocks related to rewards for agent learning.
'''

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from result import Result, Err


T = TypeVar('T')

class Reward(ABC, Generic[T]):
    '''
    Class that manages rewards in agent learning.

    Generics:
        T : something that represents a value inside of a reward
    '''

    @abstractmethod
    def set_(self, value: T, **kwargs: Any) -> Result[None, ValueError]:
        '''
        Sets the value of this reward to a value.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def get(self, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Sets the value of this reward to a value.
        '''
        return Err(ValueError(NotImplementedError))
    