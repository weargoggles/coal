#!/usr/bin/python

__doc__ = """The coal hole is where you find coal"""

from graphite.storage import Store

DEFAULT_COAL_HOLE="/opt/graphite/storage/whisper"

class Node(object):
    """Nodes are collected data: Furnaces burn them"""
    def __init__(self, bucket):
        self.metric = bucket.metric_path


class Hole(object):
    """The Hole wraps up a graphite.Store and gives you Coal"""
    def __init__(self, hostname=False, directory=DEFAULT_COAL_HOLE):
        if hostname:
            self.store = Store(remote_hosts=[hostname])
        elif directory:
            self.store = Store(directories=[directory])
        else:
            raise ValueError, "hostname or directory required"

    def get_coal(self, branch='*', max_depth=9, depth=0):
        for bucket in self.store.find_all(branch):
            if bucket.isLeaf():
                yield Node(bucket)
            else:
                if depth < max_depth:
                    for _bucket in self.get_coal(branch = bucket.metric_path + '.*', depth = depth + 1):
                        yield Node(_bucket)
