from slackclient import SlackClient
#from sets import Set
import json
from django.conf import settings
import os
from boto.s3.connection import S3Connection
import boto
from boto.s3.key import Key


class SlackUtil:
    """
    This is the class for slack api calls

    """
    

    def __init__(self):
     """"
     non parameterized constructor

     accessing S3 bucket and retrieving google service json file

     """ 

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
      """
       return list of channels 

       Returns
       -------
       list 
         the list of channels

      """

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
        """
        return list of messages given  channelCode
        Parameters
        -----------
        channelCode : str
             the channel code
        Returns
        -------
        list
          the list of messages in the channel

        """

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
        """"
        return messages given user_id and channel code

        Parameters
        -------
        channelCode : str
             the channel code
        user_id : str
             user id 

        Returns
        -------
        list
           list of user messages in the channel         
        """

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


    

    def getUserById(self,user_id):
        """"
         returns the user name given user_iod

         Parameters
         -----------
         user_id : str
           user id 

        Returns
        -----------
         str
            username   

        """
        user = self.sc.api_call(
            "users.profile.get",
            user=user_id,
            limit=100
        )

        profile = user["profile"]
        user_name = profile["real_name"]
        return user_name

    def getChannelById(self, channel_id):
        """
         returns the channel name given channel id
         Parameters
         ---------
         channel_id : str
             channel id

         Returns
         ------
         str
            channel_name    
        """
        channel = self.sc.api_call(
        "channels.info",
        channel=channel_id
        #include_locale=true
        )  
        channel_name = channel["channel"]["name"]
        return channel_name

    def getRepliesByThreadId(self,channel_id,thread_id):
        """"
         returns the replies given the thread id.

         Parameters
         ----------
         channel_id : str
              channel_id
         thread_id : str
              thread_id

         Returns
         ------
         list
           list of messages           

        """

        threadMessages = self.sc.api_call(
        "conversations.replies",
        channel=channel_id,
        ts=thread_id
        #inclusive=true
        ) 
        
        messages = threadMessages["messages"]
        threadSpecificMessages = {}
        profiles = {}
        for message in messages:
            if "client_msg_id" in message:
                  message["id"] = message['client_msg_id']    
            if "bot_id"  in message:
                  message["id"] = message['bot_id']
            if not "reply_count" in message:
               threadSpecificMessages.update({message['id']:message})
               if "user" in message:
                if message['user'] in profiles:
                   message['profile'] = profiles[message['user']]
                else:
                   profiles[message['user']] = self.getUserById(message['user'])
                   message["profile"] = profiles[message['user']]
        return threadSpecificMessages


