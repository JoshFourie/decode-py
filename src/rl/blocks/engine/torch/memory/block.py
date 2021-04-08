'''
The `.torch.memory.block` module wraps the widget and engine components in a MemoryBlock.
'''

from src.showcase.interface import Display

from typing import Any, Generic, List, Sequence, TypeVar
from result import Result, Err, Ok
from typing_extensions import TypeAlias

from ....interface import MemoryBlock
from .engine import ReplayMemoryBatch, ReplayMemory, ReplayMemoryFactory

import pandas as pd
import streamlit as st


T = TypeVar('T')

Parent: TypeAlias = Any
Children: TypeAlias = Sequence[Display[Any, Any, Any]]

Engine: TypeAlias = ReplayMemory[T, ReplayMemoryBatch[T]]
Factory: TypeAlias = ReplayMemoryFactory[T, ReplayMemoryBatch[T]]
Block: TypeAlias = MemoryBlock[T, Parent, Children, Engine]

class ReplayMemoryBlock(Generic[T], Block[T]):
    '''
    Widget for displaying a ReplayMemory in a MemoryBlock.

    Generics:
        T : some type to be stored in a ReplayMemoryBlock.
    '''

    make = Factory[T]

    __engine__: Engine[T]
    
    def __init__(self, engine: Engine[T], **kwargs: Any) -> None:
        '''
        Wraps a memory instance in the block.
        '''
        self.__engine__ = engine

    def engine(self, **kwargs: Any) -> Result[Engine[T], ValueError]:
        '''
        Returns a ReplayMemory instance.
        '''
        return Ok(self.__engine__)


    def display(self, parent: Parent, children: Children, **kwargs: Any) -> Result[Any, ValueError]:
        '''
        Displays a Memory[T] item.
        '''
        # set up components

        try: return Ok(None)

        except ValueError as error: return Err(ValueError(error, 'displaying ReplayMemoryBlock failed'))

    def update(self, parent: Parent, children: Children, **kwargs: Any) -> Result[Any, ValueError]:
        '''
        Updates the ReplayMemoryBlock display.
        '''
        try: 
            rewards = list()

            for observation in self.engine().unwrap():
                rewards.append(observation.engine().unwrap().get_reward().unwrap())

            parent.area_chart(rewards)

            return Ok(None)
        except ValueError as error: return Err(ValueError(error, 'updating ReplayMemoryBlock failed.'))
