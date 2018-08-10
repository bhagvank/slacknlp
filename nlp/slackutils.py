from slackclient import SlackClient
#from sets import Set
import json
from django.conf import settings
import os
from boto.s3.connection import S3Connection
import boto
from boto.s3.key import Key


class SlackUtil:

    

    def __init__(self):

     self.data = []
     self.slack_token = os.environ['SLACK_TOKEN']
     self.sc = SlackClient(self.slack_token)
     #print("slack client", self.sc)
     kwargs = {'aws_access_key_id': os.environ['ACCESS_KEY_ID'], 'aws_secret_access_key': os.environ['SECRET_ACCESS_KEY']}   
     conn = boto.s3.connect_to_region(os.environ['AWS_REGION'],**kwargs)
     bucket = conn.get_bucket('googleservicejson')
     keyBucket = Key(bucket,'service.json')
     keyBucket.get_contents_to_filename(os.environ['GOOGLE_SERVICE'])
       

    def listChannels(self):

      listChannels = self.sc.api_call(
        "channels.list",
        exclude_archived=1
      )
      #print("listChannels",listChannels)
      channels = []

      for channel in listChannels["channels"]:

        slackChannel = {}
        slackChannel["name"] = channel["name"]
        slackChannel["id"] = channel["id"]
        channels.append(slackChannel)
      #print(channels)  
      return channels

    def listMessages(self, channelCode):

        messagesList = self.sc.api_call(
            "conversations.history",
            channel=channelCode,
            limit=100
        )
        #print("messagesList",messagesList)
        messages = {}

        profiles = {}

        #channels = {}

        channel = self.getChannelById(channelCode)

        for message in messagesList["messages"]:

            channelMessage = {}
            channelMessage["text"] = message['text']
            channelMessage["channel_id"] = channelCode
            channelMessage["channel"] = channel
            
            #print("channel Message", channelMessage)
            if "user" in message:
                channelMessage["user"] = message['user']
                if message['user'] in profiles:
                   channelMessage['profile'] = profiles[message['user']]
                else:
                   profiles[message['user']] = self.getUserById(message['user'])
                   channelMessage["profile"] = profiles[message['user']]
            if "username" in message:
                channelMessage["user"] = message['username']
                

                  

            if "thread_ts" in message:
                channelMessage["thread_ts"] = message['thread_ts']
            if "ts" in message:
                channelMessage["ts"] = message["ts"]
            if "client_msg_id" in message:
               channelMessage["id"] = message['client_msg_id']    
               messages.update({message['client_msg_id']: channelMessage})
            if "bot_id"  in message:
                channelMessage["id"] = message['bot_id']
                messages.update({message['bot_id']: channelMessage}) 

                

        #print("channelMessages", messages)

        return messages

    def getMessagesByUser(self, channelCode,user_id):

        messagesList = self.sc.api_call(
            "conversations.history",
            channel=channelCode,
            limit=100
        )
        #print("messagesList",messagesList)
        messages = {}

        profiles = {}

        #channels = {}

        channel = self.getChannelById(channelCode)

        for message in messagesList["messages"]:

            channelMessage = {}
            channelMessage["text"] = message['text']
            channelMessage["channel_id"] = channelCode
            channelMessage["channel"] = channel
            
            #print("channel Message", channelMessage)
            if "user" in message:
                channelMessage["user"] = message['user']
                if message['user'] in profiles:
                   channelMessage['profile'] = profiles[message['user']]
                else:
                   profiles[message['user']] = self.getUserById(message['user'])
                   channelMessage["profile"] = profiles[message['user']]
            if "username" in message:
                channelMessage["user"] = message['username']
                

                  

            if "thread_ts" in message:
                channelMessage["thread_ts"] = message['thread_ts']
            if "ts" in message:
                channelMessage["ts"] = message["ts"]

            if channelMessage['user'] == user_id:

               if "client_msg_id" in message:
                  channelMessage["id"] = message['client_msg_id']    
                  messages.update({message['client_msg_id']: channelMessage})
               if "bot_id"  in message:
                  channelMessage["id"] = message['bot_id']
                  messages.update({message['bot_id']: channelMessage}) 

                

        #print("channelMessages", messages)

        return messages


    def groupThreadMessagesByUser(self, messages):

        #users = []
        threads = []
        allmessages = []
        channels = {}

        for key,value in messages.items():
            #channel = key
            message = value
            #message["channel_id"] = channel
            #if channel in channels:
            #   message["channel"] = channels[channel]
            #else:
            #   channels[channel] = self.getChannelById(channel)
            #message["channel"] = channels[channel]
            allmessages.append(message)
                #print("message in grouping thread", message)
            #users.append(message["user"])
            if "thread_ts" in message:
                threads.append(message["thread_ts"])
            else:
                threads.append(message["ts"])
                    
        #userset = set(users)
        threadset = set(threads)

        #userMessages = {}
        threadMessages = {}
        #for user in userset:
        #    userMessages[user] = {}
        for thread in threadset:

            threadMessages[thread] = {}
            for message in allmessages:

                if "thread_ts" in message:
                    if message["thread_ts"] == thread:
                       threadMessages[thread].update({message["id"]: message})
                if "ts" in message:
                   if message["ts"] == thread:
                      threadMessages[thread].update({message["id"]: message})
                #userMessages[user].update({thread:threadMessages[thread]})

        return threadMessages

    def getUserById(self,user_id):
        user = self.sc.api_call(
            "users.profile.get",
            user=user_id,
            limit=100
        )

        profile = user["profile"]
        user_name = profile["real_name"]
        return user_name

    def getChannelById(self, channel_id):
        channel = self.sc.api_call(
        "channels.info",
        channel=channel_id
        #include_locale=true
        )  
        channel_name = channel["channel"]["name"]
        return channel_name

    def getRepliesByThreadId(self,channel_id,thread_id):

        threadMessages = self.sc.api_call(
        "conversations.replies",
        channel=channel_id,
        ts=thread_id
        #inclusive=true
        ) 
        
        messages = threadMessages["messages"]
        threadSpecificMessages = []
        profiles = {}
        for message in messages:
            if not "reply_count" in message:
               threadSpecificMessages.append(message)
               if "user" in message:
                if message['user'] in profiles:
                   message['profile'] = profiles[message['user']]
                else:
                   profiles[message['user']] = self.getUserById(message['user'])
                   message["profile"] = profiles[message['user']]
        return threadSpecificMessages


