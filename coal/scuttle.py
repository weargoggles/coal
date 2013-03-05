"""These are like dashboards. They hold Coal for the Furnaces and receive Soot"""

from coal.hole import Hole
import coal.config

class Bucket(object):
    def __init__(self):
        pass

class Cooper(object):
    """Makes buckets"""
    def __init__(self):
        if coal.config.host:
            self.coal_hole = Hole(hostname=coal.config.host)
        elif coal.config.directory:
            self.coal_hole = Hole()

class AggregateBucket(Bucket):
    "Aggregate bucket for global-level soot"
    pass

class HostBucket(Bucket):
    """Host buckets for host-specific soot"""
    pass
