'''
The .blocks submodule is responsible for combining the building blocks of reinforcement learning agents in .engine with visualisations in .widgets
'''

from abc import abstractmethod

from result.result import Err, Result
from typing import Any, Generic, TypeVar

from ...showcase.interface import Display


T = TypeVar('T')

U = TypeVar('U')
V = TypeVar('V')
W = TypeVar('W')
X = TypeVar('X')

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')
E = TypeVar('E')

class MemoryBlock(Generic[T, B, C, E], Display[Any, B, C]):
    '''
    Class for wrapping `.engine.Memory` subclasses with `Display[Any]`.
    '''
    
    @abstractmethod
    def engine(self, **kwargs: Any) -> Result[E, ValueError]:
        '''
        Returns the engine for this block.
        '''
        return Err(ValueError(NotImplementedError))


class ObservationBlock(Generic[U, V, W, X, B, C, D], Display[Any, B, C], ):
    '''
    Class for wrapping `.interface.Observation` subclasses with `Display[Any]`
    '''
    @abstractmethod
    def engine(self, **kwargs: Any) -> Result[D, ValueError]:
        '''
        Returns the engine for this block.
        '''
        return Err(ValueError(NotImplementedError))

