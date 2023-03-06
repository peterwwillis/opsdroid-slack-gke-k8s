import sys
import logging

from opsdroid.skill import Skill
from opsdroid.matchers import match_parse, match_regex, match_crontab
from opsdroid.events import Message, Reaction, File, Image, Video, JoinRoom, LeaveRoom

from kubernetes import client, config

from . import k8s
from . import gke


_LOGGER = logging.getLogger(__name__)


class K8sGKESkill(Skill):
    k = None
    def __init__(self, opsdroid, config):
        super(K8sGKESkill, self).__init__(opsdroid, config)
        self.k = k8s.K8s()

    #@match_event(Message)
    #@match_regex(r'get cluster.*')

    @match_parse('k8s get cluster {cluster}', case_sensitive=False, matching_condition='search')
    async def get_cluster(self, event):
        cluster = message.entities['cluster']['value']
        await event.respond(cluster_list_text)

    @match_parse('k8s get clusters', case_sensitive=False, matching_condition='search')
    async def get_clusters(self, event):
        await event.respond(cluster_list_text)

