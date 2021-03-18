'''
This module implements abstract classes for blocks related to memory management for agent learning with PyTorch.
'''

from typing import Any, Generic, Iterable, Iterator, List, Sequence, TypeVar

from result.result import Err, Ok, Result
from typing_extensions import TypeAlias

from ...interface.memory import BatchMemory, MemoryFactory, IterableMemory

import random


T = TypeVar('T')
V = TypeVar('V')

ReplayMemoryBatch: TypeAlias = List[T]

class ReplayMemory(Generic[T, V], IterableMemory[T], BatchMemory[T, ReplayMemoryBatch[T]]):
    '''
    Implementation of ABC IterableMemory.

    https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

    Generics:
        T : some type of item to be stored in a memory buffer
        MemoryBatch[T]: a batch of memories of type T 
    '''

    __capacity__: int
    __memories__: List[T]
    __position__: int
    
    def __init__(self, capacity: int, memories: Sequence[T], position: int) -> None:
        '''
        Sets the class fields for this ReplayMemory instance.
        '''
        super().__init__()

        self.__capacity__ = capacity
        self.__memories__ = list(memories)
        self.__position__ = position

    def __len__(self) -> int: 
        '''
        Returns the number of memories currently stored in the object instance.
        '''
        return len(self.__memories__)

    def push(self, memory: T, **kwargs: Any) -> Result[None, ValueError]:
        '''
        Adds a memory of type T to the stack. 

        kwargs:
            overwrite : bool = False
        '''

        overwrite = kwargs.pop('overwrite', False)

        if len(self) < self.__capacity__: 
            self.__memories__.append(memory)
        elif overwrite:
            try: 
                self.__memories__[self.__position__] = memory
                self.__position__ = (self.__position__ + 1) % self.__capacity__
            except: return Err(ValueError(f'failed to overwrite entry {self.__position__} in ReplayMemory'))
        else: 
            return Err(ValueError(f'out of memory and overwrite is {overwrite}'))

        return Ok(None)

    def pop(self, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Pops a memory of type T from the stack. Calling `.pop(..)` when in the last position will keep the position as
        the last position in the new stack.
        '''
        size = len(self)
        position = self.__position__

        if size > 0:
            self.__position__ = size - 1 if position == 0 else position - 1   # if we were at the last position, jump back to end, otherwise go back one
            try: return Ok(self.__memories__.pop())
            except ValueError as error: return Err(ValueError(error, 'failed to pop memory'))
        else: return Err(ValueError('tried to pop memory from zero-length ReplayMemory'))


    def sample_one(self, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Randomly samples a memory from the stack.
        '''
        try: return Ok(random.choice(self.__memories__))
        except ValueError as error: return Err(ValueError(error, 'failed to sample a memory from the stack'))

    def sample_batch(self, size: int, **kwargs: Any) -> Result[ReplayMemoryBatch[T], ValueError]:
        '''
        Randomly samples a batch of memories from the stack.
        '''
        try:
            samples = random.sample(self.__memories__, k = size)
            return Ok(samples)
        except ValueError as error: return Err(ValueError(error, 'failed to sample a batch of memories from the stack'))

    def capacity(self) -> Result[int, ValueError]:
        '''
        Returns the total capacity of a ReplayMemory instance.
        '''
        return Ok(self.__capacity__)

    def available(self) -> Result[int, ValueError]:
        '''
        Returns the total remaining capacity of a ReplayMemory instance.
        '''
        return Ok(self.__capacity__ - len(self))

    def used(self) -> Result[int, ValueError]:
        '''
        Returns the total capacity currently in use for a ReplayMemory instance.
        '''
        return Ok(len(self))

    def __iter__(self) -> Iterator[T]: return self.__memories__.__iter__()


ReplayMemoryFactoryAlias: TypeAlias = MemoryFactory[T, ReplayMemory[T, V]]

class ReplayMemoryFactory(Generic[T, V], ReplayMemoryFactoryAlias[T, V]):
    '''
    Factory for creating ReplayMemory instances.

    Generics: T, V
        T : some type to be passed onto ReplayMemory as type T (likely a memory)
        V : some type to be passed onto ReplayMemory as type V (likely a batch of memories)
    '''

    @classmethod
    def pop_kwarg(cls, key: str, **kwargs: Any) -> Result[Any, ValueError]:
        '''
        Pops the key from a set of kew word arguments.
        '''
        try: 
            value: Any = kwargs.pop(key)    # can throw a KeyError exception
            return Ok(value)

        except ValueError as error: return Err(ValueError(error, f'failed to find {key} in {kwargs}'))

    @classmethod
    def new(cls, **kwargs: Any) -> Result[ReplayMemory[T, V], ValueError]:
        '''
        Returns a new ReplayMemory instance.

        kwargs:
            capacity : int
        '''
        values: Sequence[T] = list()
        return ReplayMemoryFactory.from_sequence(values, **kwargs)

    @classmethod
    def from_iterator(cls, iterator: Iterable[T], **kwargs: Any) -> Result[ReplayMemory[T, V], ValueError]:
        '''
        Returns a ReplayMemory object from an iterator of memories.
        '''
        values: Sequence[T] = list(iterator)
        return ReplayMemoryFactory.from_sequence(values, **kwargs)

    @classmethod
    def from_sequence(cls, sequence: Sequence[T], **kwargs: Any) -> Result[ReplayMemory[T, V], ValueError]:
        '''
        Returns a ReplayMemory object from a Sequence of memories.

        kwargs:
            position : int = 0
        '''
        try: capacity = ReplayMemoryFactory.pop_kwarg('capacity', **kwargs).expect('expected kwarg for capacity')
        except ValueError as error: return Err(error)

        try: 
            position: int = kwargs.pop('position', 0)

            memory: ReplayMemory[T, V] = ReplayMemory(capacity = capacity, memories = sequence, position = position)
            return Ok(memory)

        except Exception as error: return Err(ValueError(error, 'failed to create ReplayMemory instance.'))
