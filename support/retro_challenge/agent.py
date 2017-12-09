import argparse
import gym_remote.exceptions as gre
import gym_remote.client as grc
import os
import sys
import traceback
from pkg_resources import EntryPoint


def make(socketdir='tmp/sock'):
    env = grc.RemoteEnv(socketdir)
    return env


def run(agent=None, socketdir='tmp/sock', daemonize=False, *args):
    if daemonize:
        pid = os.fork()
        if pid > 0:
            return

    if agent is None:
        agent = random_agent
    elif not callable(agent):
        entrypoint = EntryPoint.parse('entry=' + agent)
        agent = entrypoint.load(False)
    env = make(socketdir)
    try:
        agent(env)
    except gre.GymRemoteError:
        pass


def random_agent(env):
    env.reset()
    while True:
        action = env.action_space.sample()
        ob, reward, done, _ = env.step(action)
        if done:
            env.reset()


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Run support code for Retro Challenge remote environment')
    parser.add_argument('--daemonize', '-d', action='store_true', default=False, help='Daemonize (background) the process')
    parser.add_argument('entry', type=str, nargs='?', help='Entry point to create an agent')
    parser.add_argument('args', nargs='*', help='Optional arguments to the agent')

    args = parser.parse_args(argv)
    run(agent=args.entry, daemonize=args.daemonize, *args.args)

if __name__ == '__main__':
    main()
