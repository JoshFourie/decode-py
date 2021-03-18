'''
This module adds abstract classes for blocks related to memory management for agent learning.
'''

from abc import ABC, abstractmethod, abstractclassmethod
from typing import Any, Generic, Iterable, Iterator, Sequence, TypeVar

from result import Result, Err


T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

class Memory(ABC, Generic[T]):
    '''
    The abstract base class for memory objects.
    '''

    @abstractmethod
    def push(self, memory: T, **kwargs: Any) -> Result[None, ValueError]: 
        '''
        Adds a memory of generic type T to the stack.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def pop(self, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Pops a memory of type T from the stack.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def sample_one(self, **kwargs: Any) -> Result[T, ValueError]:
        '''
        Samples a random memory of type T from the stack.
        '''
        return Err(ValueError(NotImplementedError))
 
    @abstractmethod
    def capacity(self) -> Result[int, ValueError]:
        '''
        Returns the total capacity of a memory instance.
        '''
        return Err(ValueError(NotImplementedError))
        
    @abstractmethod
    def available(self) -> Result[int, ValueError]:
        '''
        Returns the total remaining available capacity of a memory instance.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractmethod
    def used(self) -> Result[int, ValueError]:
        '''
        Returns the total capacity currently in use for a memory instance.
        '''
        return Err(ValueError(NotImplementedError))


class BatchMemory(Generic[T, V], Memory[T]):
    '''
    Extension of Memory ABC to allow for batched sampling.

    Generics:
        T : some type to be passed onto ABC Memory 
        V : some type representing a batch of memories 
    '''

    @abstractmethod
    def sample_batch(self, size: int, **kwargs: Any) -> Result[V, ValueError]:
        '''
        Returns a sequence or iterator of memories.
        '''
        return Err(ValueError(NotImplementedError))
    

class IterableMemory(Memory[T], Iterable[T]):
    '''
    Extension of Memory ABC to allow for iterations.
    '''
    
    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        '''
        Returns an iterator over memories.
        '''
        return Err(ValueError(NotImplementedError))


class MemoryFactory(ABC, Generic[T, U]):
    '''
    Factory for creating instances of Memory classes.

    Generics:
        T : some type to be stored in the memory buffer.
        U : some type to be returned by the factory.
    '''

    @abstractclassmethod
    def new(cls, **kwargs: Any) -> Result[U, ValueError]:
        '''
        Creates a memory instance from a sequence of memories.
        '''
        return Err(ValueError(NotImplementedError))
        
    @abstractclassmethod
    def from_sequence(cls, sequence: Sequence[T], **kwargs: Any) -> Result[U, ValueError]:
        '''
        Creates a memory instance from a sequence of memories.
        '''
        return Err(ValueError(NotImplementedError))

    @abstractclassmethod
    def from_iterator(cls, iterator: Iterable[T], **kwargs: Any) -> Result[U, ValueError]:
        '''
        Creates a memory instance from an iterator of memories.
        '''
        return Err(ValueError(NotImplementedError))

