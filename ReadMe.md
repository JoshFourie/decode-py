# Zalia Flow: `Decoded`

A library for composable explainability in reinforcement learning agents.

## What's that?

Reading explanations of other people's RL agents and giving explanations of our own sucks. We want to
write and train our RL agents and then deploy that into a front-end for others to explore.

No more crawling through Python code and more focus on seeing algorithms in action.

## Who are we?
Zalia Flow ([zaliaflow.io](zaliaflow.io)) is an enterprise toolkit for building artificial intelligence that people delight in trusting. 
Our core libraries are released as open-source software.

# Getting started

Right now, you can install from source and run an example.

```
$ git clone git@github.com:ZaliaFlow/decode-py.git
$ cd decode
$ python3 -m pip install -r requirements.txt
$ cd src
$ streamlit run example/pong.py
```
## What's happening?
In `example/pong.py` is the `hello-world` of reinforcement learning: a random agent sampling an environment.

Right now, there are two lines that matter:

```
memory = Memory(engine = Memory.make.new(capacity = 1000).unwrap())
...
memory.update(parent = memory_display, children = None).unwrap()
```

This is a high-level API for getting an experience buffer for Deep Q-Networks that will
open up a display of the agent's results from sampling the reward distribution.

## How can you help?
Help us find out what's the single most impactful view of your machine-learning code that would make it effortless to explain.

Book a meeting with our team on [https://www.zaliaflow.io/book-online](zaliaflow.io/book-online) to chat.
