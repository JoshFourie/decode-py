'''
The .blocks submodule is responsible for combining the building blocks of reinforcement learning agents in .engine with visualisations in .widgets
'''

from abc import abstractmethod, ABC

from result.result import Err, Result
from typing import Any, Generic, TypeVar

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

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')


class Display(Generic[T, U, V], ABC):
    '''
    ABC for things that can return a display to a showcase runner.

    Generics:
        T : something that can be rendered by a showcase
        U : some parent to callback to
        V : some children to callback to
    '''

    @abstractmethod
    def display(self, parent: U, children: V, **kwargs: Any) -> T:
        '''
        Displays the block in a showcase environment.
        '''
        raise NotImplementedError

    @abstractmethod
    def update(self, parent: U, children: V, **kwargs: Any) -> T:
        '''
        Updates a block in a showcase environment.
        '''
        raise NotImplementedError

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

