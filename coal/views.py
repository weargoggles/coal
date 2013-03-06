from django.shortcuts import render_to_response
from django.template import RequestContext
from coal.host import Host
from coal.source import Source

source = Source()


def root(request):
    context = {
        'hosts': source.get_hosts(),
    }
    return render_to_response("coal/root.html", context, RequestContext(request))

def host(request, hostname):
    context = {
        'host': Host(hostname)
    }