'''
The .showcase submodule is responsible for managing the displaying of the assembled components.

This file is an interface for upstream modules to interact with the .showcase module.
'''

# built-in libraries
from typing import Any, Generic, TypeVar
from abc import ABC, abstractmethod


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
