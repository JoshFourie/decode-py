"""
# Code Draft

```
import memory_stuff 
import policies
import templates
import known_environments
import gyms

from known_environments import benchmarks

from agent import AgentFactory, Senses

def showcase_pong() -> None:
    '''
    Showcase a pong game.
    '''

    agent = AgentFactory.from_template(
        template = templates.BaseDQN,
        policy = policies.Softmax,
        memory = memory_stuff.ReplayMemory,
        senses = Senses.Compose([
            Senses.VisionFactory.from_template(known_environments.PONG, frames = 2)
        ]),
        showcase = True,
        validation = benchmarks.from_template(known_environments.PONG, hardness = benchmarks.Relaxed)
    ) # get a prebuilt agent
    
    env = gyms.from_template(known_environments.PONG, validation = True) 

    try: agent.inhabit(env).train(checkpoints = True, file = './my_model.pt').validate()
    except: unrecoverable_error

    output = showcase.from_agent(agent)

    output.display()
```
"""
