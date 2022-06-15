import matplotlib.pyplot as plt
import time

from flex_environment import Environment
import itertools


def calc():
    env = Environment()
    reward, done = env.reset()

    i = 0
    while i < 1000 and not done:
        action = env.action()  # (env, reward)
        reward, done = env.step(action)


if __name__ == '__main__':
    calc()
