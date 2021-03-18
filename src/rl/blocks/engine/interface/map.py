'''
This module adds abstract class for blocks related to mapping values for agent learning.
'''

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from typing_extensions import Protocol

from result import Result, Err


T = TypeVar('T')
U = TypeVar('U')

class StateMapHook(Protocol[T]):
    '''
    Protocol for managing hooks in subclass of ABC StateMap. 
    '''

    def __call__(self, state: Any, **kwargs: Any) -> Result[T, ValueError]:
        '''
        A hook for transforming a state into value T.
        '''
        return Err(ValueError(NotImplementedError))


class StateMap(ABC, Generic[T, U]):
    '''
    Class that extends the State ABC to allow for mapping.

    Generics:
        T : something that a `StateMapHook` protocol can map a state of type `Any` into.
        U : something that `.map(..)` can return in a result.
    '''

    @abstractmethod
    def map(self, hook: StateMapHook[T]) -> Result[U, ValueError]:
        '''
        Gets a value, applies the hook and returns the result.

        Does not mutate anything in place.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def map_(self, hook: StateMapHook[T]) -> Result[None, ValueError]:
        '''
        Maps a value in place by applying the hook. 
        '''
        return Err(ValueError(NotImplementedError))

