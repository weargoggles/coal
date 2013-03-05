#!/usr/bin/python

import os
import sys
import subprocess
import pickle
import json
import re

COAL_CONFIG_DIR = os.getenv('COAL_CONFIG_DIR', '/etc/coal')
COAL_FURNACE_DIR = os.getenv('COAL_FURNACE_DIR', os.path.join(COAL_CONFIG_DIR,'furnaces'))
COAL_FURNACE_CONFIG = os.path.join(COAL_CONFIG_DIR, 'furnaces.pickle')


class FurnaceException(Exception):
    pass


class Furnace(object):
    def __init__(self, name, mode):
        cmd = subprocess.Popen(
            [os.path.join(COAL_FURNACE_DIR, name), '--'+mode+'-config'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = cmd.wait()
        if r not in [0,2]:
            raise FurnaceException, "The furnace %s did not exit cleanly - ignoring it." % name
        elif r == 2:
            pass # The furnace does not provide config for the requested mode
        else:
            self.matchers = []
            config_loaded = json.load(cmd.stdout)
            self.title = config_loaded['title'] or name
            self.category = config_loaded['category'] or name
            self.description = config_loaded['description'] or ''
            for matcher in config_loaded['chutes']:
                self.matchers.append(re.compile(matcher))
            

    def matches(self, node):
        for matcher in self.matchers:
            if matcher.search(node.metric) is not None:
                return True

    def process(self, nodes):
        pass


def reload_installed_furnaces():
    try:
        furnace_scripts = sorted(os.listdir(COAL_FURNACE_DIR))
    except Exception:
        sys.stderr.write("Couldn't list " + COAL_FURNACE_DIR)
        sys.exit(1)

    global_furnaces = {}
    host_furnaces = {}

    for script in furnace_scripts:
        try:
            host_furnaces[script] = Furnace(script, 'host')
            global_furnaces[script] = Furnace(script, 'global')
        except FurnaceException:
            pass

    config = {
        'global': global_furnaces,
        'host': host_furnaces
    }

    with open(COAL_FURNACE_CONFIG, 'w') as f:
        pickle.dump(config, f)

    return config

def get_installed_furnaces():
    with open(COAL_FURNACE_CONFIG, 'r') as f:
        return pickle.load(f)


