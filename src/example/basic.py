'''
Basic example of a displayable neural net with inferred composability.
'''

import sys; sys.path.append('../')  # silly hack to get the zalia package

# library imports
from src.showcase.broadcast.simple import SimpleBroadcastFacade, SimpleGraphKey, SimpleGraphMemento
from src.showcase.database.simple import SimpleGraphDB

# external imports
import gym

'''
Set up broadcast facade.
'''
graph: SimpleGraphDB[SimpleGraphKey, SimpleGraphMemento] = SimpleGraphDB()

facade: SimpleBroadcastFacade[SimpleGraphMemento] = SimpleBroadcastFacade(graph = graph)

'''
Set up a computation.
'''