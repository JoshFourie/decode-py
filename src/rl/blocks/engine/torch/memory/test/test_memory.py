'''
This module tests pytorch implementations of ABCs related to memory management.
'''

from typing import Sequence

from ..engine import ReplayMemory, ReplayMemoryFactory

def test_replay_factory() -> None:
    '''
    Tests that ReplayMemory can be created by ReplayMemoryFactory.
    '''
    t1 = ReplayMemoryFactory.from_sequence([0, 1, 2, 3], capacity = 4).unwrap()

    assert t1.capacity().unwrap() == 4
    assert t1.available().unwrap() == 0
    assert t1.used().unwrap() == 4

    t2 = ReplayMemoryFactory.from_iterator(range(0, 3), capacity = 4).unwrap()

    assert t2.capacity().unwrap() == 4
    assert t2.available().unwrap() == 1
    assert t2.used().unwrap() == 3

    t3 = ReplayMemoryFactory.new(capacity = 4).unwrap()

    assert t3.capacity().unwrap() == 4
    assert t3.available().unwrap() == 4
    assert t3.used().unwrap() == 0
    
def test_push() -> None:
    '''
    Tests that ReplayMemory can have memories pushed to the stack.
    '''
    memory: ReplayMemory[int, None] = ReplayMemoryFactory[int, None].new(capacity = 4).unwrap()
    exp_generator = range(0, 4)

    for i in exp_generator: memory.push(i).unwrap()

    for test, exp in zip(exp_generator, memory): assert test == exp

def test_pop() -> None:
    '''
    Tests that ReplayMemory can pop memories off the stack.
    '''
    test_seq: Sequence[int] = list([0, 1, 2, 3, 4])
    memory: ReplayMemory[int, None] = ReplayMemoryFactory[int, None].from_sequence(test_seq, capacity = 5).unwrap()

    for test in reversed(test_seq): assert test == memory.pop().unwrap()

def test_stochastic_sample_one() -> None:
    '''
    Tests that ReplayMemory can sample one memory from the stack.
    '''
    test_seq: Sequence[int] = list([0, 1, 2, 3, 4])
    memory: ReplayMemory[int, None] = ReplayMemoryFactory[int, None].from_sequence(test_seq, capacity = 5).unwrap()

    assert memory.sample_one().unwrap() in test_seq

def test_stochastic_sample_batch_() -> None:
    '''
    Tests that ReplayMemory can sample a batch of memories from the stack.
    '''
    test_seq: Sequence[int] = list([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    memory: ReplayMemory[int, Sequence[int]] = ReplayMemoryFactory[int, Sequence[int]].from_sequence(test_seq, capacity = 10).unwrap()

    batch = memory.sample_batch(4).unwrap()

    for item in batch: assert item in test_seq

    assert len(batch) == 4

def test_iter() -> None:
    '''
    Tests that ReplayMemory can act as an iterable.
    '''
    test_seq: Sequence[int] = list([0, 1, 2, 3, 4])
    memory: ReplayMemory[int, None] = ReplayMemoryFactory[int, None].from_sequence(test_seq, capacity = 5).unwrap()

    for i, j in zip(test_seq, memory): assert i == j

def test_overwrite() -> None:
    '''
    Tests that ReplayMemory can overwrite old memories.
    '''
    memory: ReplayMemory[int, None] = ReplayMemoryFactory[int, None].from_sequence([0, 1, 2, 3], capacity = 5).unwrap()

    for i in [4, 5, 6]: memory.push(i, overwrite = True)

    assert memory.__memories__ == [5, 6, 2, 3, 4]

def test_pop_on_last_position() -> None:
    '''
    Tests that ReplayMemory can find the correct position after a pop on the last position.
    '''
    memory: ReplayMemory[int, None] = ReplayMemoryFactory[int, None].from_sequence([0, 1, 2, 3], capacity = 4).unwrap()

    assert memory.__memories__ == [0, 1, 2, 3]
    assert memory.__position__ == 0

    memory.pop().unwrap()

    assert memory.__memories__ == [0, 1, 2]
    assert memory.__position__ == 3