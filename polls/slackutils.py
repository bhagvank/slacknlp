from slackclient import SlackClient
#from sets import Set
import json


class SlackUtil:

    

    def __init__(self):

     self.data = []
     self.slack_token = "xoxp-399005362672-399475669492-401042564614-6319e85654d14062c29cb4169bb57138"
     self.sc = SlackClient(self.slack_token)

    def listChannels(self):

      listChannels = self.sc.api_call(
        "channels.list",
        exclude_archived=1
      )
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

        for message in messagesList["messages"]:

            channelMessage = {}
            channelMessage["text"] = message['text']
            channelMessage["channel"] = channelCode
            
            #print("channel Message", channelMessage)
            if "user" in message:
                channelMessage["user"] = message['user']
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



    def groupThreadMessagesByUser(self, messages):

        users = []
        threads = []
        allmessages = []
        for key,value in messages.items():

            channelMessages = value
            for key,value in channelMessages.items():
                message = value
                allmessages.append(message)
                #print("message in grouping thread", message)
                users.append(message["user"])
                if "thread_ts" in message:
                    threads.append(message["thread_ts"])
                else:
                    threads.append(message["ts"])
                    
        userset = set(users)
        threadset = set(threads)

        userMessages = {}
        threadMessages = {}
        for user in userset:
            userMessages[user] = {}
            for thread in threadset:

                threadMessages[thread] = {}
                for message in allmessages:

                    if "thread_ts" in message:
                       if message["user"] == user and message["thread_ts"] == thread:
                          threadMessages[thread].update({message["id"]: message})
                    if "ts" in message:
                       if message["user"] == user and message["ts"] == thread:
                           threadMessages[thread].update({message["id"]: message})
                userMessages[user].update({thread:threadMessages[thread]})

        return userMessages

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
        for message in messages:
            if not "reply_count" in message:
               threadSpecificMessages.append(message)
        return threadSpecificMessages


