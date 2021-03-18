'''
The `.torch.memory.test.show_memory` module lets us display some of the MemoryBlocks.
'''
import sys; sys.path.append('../')  # silly hack to get the zalia package

from src.rl.blocks import ReplayMemoryBlock

import streamlit as st

'''
# PyTorch: ReplayMemoryBlock.
'''

try:
    memory = ReplayMemoryBlock(
        engine = ReplayMemoryBlock[int].make.from_sequence([0, 1, 2, 3, 4, 5], capacity = 10).unwrap()
    )
except ValueError as error: raise error
