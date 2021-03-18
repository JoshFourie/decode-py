'''
This module adds abstract classes for blocks related to actions for agent learning.
'''

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from result import Result, Err


T = TypeVar('T')

class Action(ABC, Generic[T]):
    '''
    Class that manages actions in agent learning.
    '''

    @abstractmethod
    def set(self, value: T, **kwargs: Any) -> Result[None, ValueError]:
        '''
        Sets the value of this action to a value of type T.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def get(self, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Sets the value of this action to a value of type T.
        '''
        return Err(ValueError(NotImplementedError))
    