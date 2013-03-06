#!/usr/bin/python

import os
import sys
import subprocess
import pickle
import json
import re
from coal.graph import Graph

COAL_CONFIG_DIR = os.getenv('COAL_CONFIG_DIR', '/etc/coal')
COAL_PROCESSOR_DIR = os.getenv('COAL_PROCESSOR_DIR', os.path.join(COAL_CONFIG_DIR, 'processors'))
COAL_PROCESSOR_CONFIG = os.path.join(COAL_CONFIG_DIR, 'processors.pickle')


class ProcessorException(Exception):
    pass


class Processor(object):
    config = {
        'aggregate': {},
        'host': {},
    }
    host_processors = config['host']
    aggregate_processors = config['aggregate']

    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        cmd = subprocess.Popen(
            [os.path.join(COAL_PROCESSOR_DIR, self.name), '--' + self.mode + '-config'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        r = cmd.wait()
        if r not in [0, 2]:
            raise ProcessorException("The processor %s did not exit cleanly - ignoring it." % self.name)
        elif r == 2:
            pass  # The furnace does not provide config for the requested mode
        else:
            self.match_expressions = []
            config_loaded = json.load(cmd.stdout)
            self.title = config_loaded['title'] or self.name
            self.category = config_loaded['category'] or self.name
            self.description = config_loaded['description'] or ''
            for matcher in config_loaded['match_expressions']:
                self.match_expressions.append(re.compile(matcher))

    def matches(self, node):
        for match_expression in self.match_expressions:
            if match_expression.search(node.metric) is not None:
                return True

    def process(self, nodes):
        """feed the list of nodes to the executable. the executable should respond with a set of
        graphs, as a an array of hashes."""
        cmd = subprocess.Popen(
            [os.path.join(COAL_PROCESSOR_DIR, self.name), '--' + self.mode],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        )
        json.dump([node.metric for node in nodes], cmd.stdin)
        r = cmd.wait()
        if r not in [0, 2]:
            raise ProcessorException("The processor %s did not exit cleanly while processing nodes" % self.name)
        elif r == 2:
            pass
        else:
            graph_hashes = json.load(cmd.stdout)
            return [Graph.from_hash(g) for g in graph_hashes]

    @classmethod
    def reload_processors(cls):
        try:
            processors = sorted(os.listdir(COAL_PROCESSOR_DIR))
        except IOError:
            sys.stderr.write("Couldn't list " + COAL_PROCESSOR_DIR)
            sys.exit(1)

        for script in processors:
            for mode in cls.config.keys():
                try:
                    cls.config[mode][script] = cls(script, mode)
                except ProcessorException:
                    pass

    @classmethod
    def save_config(cls):
        with open(COAL_PROCESSOR_CONFIG, 'w') as f:
            pickle.dump(cls.config, f)

    @classmethod
    def load_config(cls):
        with open(COAL_PROCESSOR_CONFIG, 'r') as f:
            cls.config = pickle.load(f)



