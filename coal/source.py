#!/usr/bin/python

__doc__ = """The coal hole is where you find coal"""

from graphite.storage import Store

DEFAULT_COAL_HOLE = "/opt/graphite/storage/whisper"
DEFAULT_HOST_GLOB = "carbon.*"


class Node(object):
    """Nodes are collected data: Processors accept them"""

    def __init__(self, bucket):
        self.metric = bucket.metric_path


class Source(object):
    """The Source wraps up a graphite.Store and gives you Coal"""

    def __init__(self, hostname=False, directory=DEFAULT_COAL_HOLE):
        if hostname:
            self.store = Store(remote_hosts=[hostname])
        elif directory:
            self.store = Store(directories=[directory])
        else:
            raise ValueError, "hostname or directory required"

    def get_nodes(self, bucket='*', max_depth=9, depth=0):
        for bucket in self.store.find_all(bucket):
            if bucket.isLeaf():
                yield Node(bucket)
            else:
                if depth < max_depth:
                    for node in self.get_nodes(bucket=bucket.metric_path + '.*', depth=depth + 1):
                        yield node

    def get_hosts(self, glob=DEFAULT_HOST_GLOB):
        return [host for host in self.store.find_all(glob)]
