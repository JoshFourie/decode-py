'''
Basic example of a component neural net with inferred composability.
'''

import sys; sys.path.append('../')  # silly hack to get the zalia package

# library imports
from src.showcase.maker.simple import SimpleMakerFacade, SimpleGraphKey, SimpleGraphMemento
from src.showcase.database.simple import SimpleGraphDB

# external imports
import gym

'''
Set up maker facade.
'''
graph: SimpleGraphDB[SimpleGraphKey, SimpleGraphMemento] = SimpleGraphDB()

facade: SimpleMakerFacade[SimpleGraphMemento] = SimpleMakerFacade(graph = graph)

'''
Set up a computation.
'''

# @TODO.