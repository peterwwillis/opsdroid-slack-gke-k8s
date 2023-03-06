#!/usr/bin/env python3

import os
import sys
import logging

from kubernetes import client, config
from kubernetes.client import Configuration

_LOGGER = logging.getLogger(__name__)

class K8s:
    global _LOGGER
    def __init__(self):
        kube_config = os.getenv('KUBE_CONFIG')
        context = os.getenv('CONTEXT')
        config.load_kube_config(config_file=kube_config, context=context)
        client.Configuration._default.proxy = os.environ.get('HTTPS_PROXY', None)

    def kcli_get_client(self, context=None):
        """ Takes an optional context object returned from kcli_get_context().
            Returns the k8s client object """
        _LOGGER.debug("kcli_get_client(self,%s)" % context)
        selected, api_client = None, None
        if context != None:
            api_client = config.new_client_from_config(context=context)
        selected = client.CoreV1Api(api_client=api_client)
        return selected

    def kcli_list_ns(self, client):
        _LOGGER.debug("kcli_list_ns(self,%s)" % client)
        return client.list_namespace()

    def kcli_get_contexts(self):
        _LOGGER.debug("kcli_get_contexts()")
        contexts, active_context = config.list_kube_config_contexts()
        contexts = [context['name'] for context in contexts]
        return contexts, active_context

    def kcli_get_context(self, name):
        _LOGGER.debug("kcli_get_context(self, '%s')" % name)
        contexts, active_context = config.list_kube_config_contexts()
        _LOGGER.debug("contexts: '%s', active_context: '%s'" % (contexts, active_context))
        for context in contexts:
            if name == context['name']:
                _LOGGER.debug("found '%s', returning context" % name)
                return context
        return None

def k8smain():
    o = K8s()
    cli = o.kcli_get_client()
    ns = o.kcli_list_ns(cli)
    _LOGGER.info("found namespaces: '%s'" % [x.metadata.name for x in ns.items] )

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    k8smain()
