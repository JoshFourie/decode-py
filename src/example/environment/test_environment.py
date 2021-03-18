from typing import Any, Callable

from result.result import Err, Ok, Result
from .environment import GymEnvironment, Environment

from ..experience.replay import Observation, ReplayMemory

from ..policy.e_greedy import eGreedy
from ..net.DQN import CNN
from ..learner.qclone import Learner

import torch

from torch import Tensor
from torchvision.transforms import Compose, Resize, ToPILImage, ToTensor


def post_step_hook(next_state: Any, reward: Any, done: bool, info: Any, **kwargs: Any) -> Result[Any, ValueError]:
    '''
    StepHook function that maps the next_state item into a Tensor.
    '''
    try:
        net: Any = kwargs.get('net')
        processed: Any = getattr(net, 'preprocess')(next_state).expect('failed to preprocess next_state')
        return Ok((processed, reward, done))
    except ValueError as error: return Err(error)
        


def test_render() -> None:
    '''
    Renders an on-screen openai gym environment.
    '''

    env = GymEnvironment(Environment.PONG)
    actions_n = env.actions_n()

    policy = eGreedy(actions_n)
    env.set_policy(policy).expect('failed to set the policy.')

    transform: Callable[..., Tensor] = Compose([ToPILImage(), Resize((160, 210)), ToTensor()])
    online_net = CNN(width = 160, height = 420, outputs = actions_n)
    online_net.set_preprocessor(transform).expect('failed to set preprocessor')
    learner = Learner(online_net)

    try:
        state = env.reset().expect('failed to reset the environment')

        state: Tensor = online_net.preprocess(state).expect('failed to preprocess state')

        frame = torch.cat([state, state], dim=2)

        trajectory = ReplayMemory(capacity = 200)

        for i_ in range(2):    
            '''
            The main training loop.
            '''
            # env.render().expect('error whilst rendering the environment')
            env.reset().expect('failed to reset environment')
            
            frame = torch.stack([frame])

            action: int = env.apply_policy(frame, online_net, dim = 1).expect('failed to sample an action')
            next_state, reward, done = env.step(action, post_step_hook, net = online_net).expect('failed to step the environment')                   

            frame = torch.cat([state, next_state], dim=2)

            trajectory.push(Observation(
                state = state, 
                action = Tensor([action]), 
                next_state = frame, 
                reward = Tensor([reward])
            ))

            state = next_state

        batch = trajectory.sample_batch(2).expect(f'failed to sample batch')

        learner.epoch(batch)

    finally: env.close()