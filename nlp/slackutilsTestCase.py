from django.test import TestCase
from django.conf import settings
import os
import logging


class slackutilsTestCase(TestCase):

    def setUp(self): 
     self.slack_token = os.environ['SLACK_TOKEN']  

    def test_get_channels(self):


     self.sc = SlackClient(self.slack_token)   
     listChannels = self.sc.api_call(
        "channels.list",
        cursor=nextCursor,
        limit=count,
        exclude_archived=1)
     self.assertEqual(True,len(listChannels["channels"]) >0)                                                                                                                                                                                                            