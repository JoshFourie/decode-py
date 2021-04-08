'''
The .showcase submodule is responsible for managing the displaying of the assembled components.

This file is an interface for upstream modules to interact with the .showcase module.
'''

from typing import Any, Generic, TypeVar

from abc import ABC, abstractmethod

from result import Result, Err


T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')


class Display(ABC, Generic[T, U, V]):
    '''
    ABC for things that can return a display to a showcase runner.

    Generics:
        T : something that can be rendered by a showcase
        U : some parent to callback to
        V : some children to callback to
    '''

    @abstractmethod
    def display(self, parent: U, children: V, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Displays the block in a showcase environment.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def update(self, parent: U, children: V, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Updates a block in a showcase environment.
        '''
        return Err(ValueError(NotImplementedError))
