#!/usr/bin/env python3

import os
import sys
import logging

import asyncio

from google.cloud import container_v1

_LOGGER = logging.getLogger(__name__)

class GKE:
    global _LOGGER
    def __init__(self):
        return

    async def list_clusters(self, client):
        _LOGGER.debug("list_clusters(self,%s)" % client)
        request = container_v1.ListClustersRequest()
        response = await client.list_clusters(request=request)
        return response

    async def get_client(self):
        _LOGGER.debug("get_client(self)")
        selected, api_client = None, None
        selected = container_v1.ClusterManagerAsyncClient()
        return selected

async def list_clusters():
    o = GKE()
    cli = await o.get_client()
    clusters = await o.list_clusters(cli)
    _LOGGER.info("found clusters: '%s'" % clusters)

async def gkemain():
    await list_clusters()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run( gkemain() )
