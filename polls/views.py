from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader
from .models import Question, Choice
from .slackutils import SlackUtil
from .NLPUtils import NLPUtil

def index(request):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    slack = SlackUtil()
    channels = slack.listChannels()
    # messages = listMessages("CBR05AS5N")
    template_name = 'polls/index.html'
    context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name, context)

def detail(request, channel_id):
    #return HttpResponse("You're looking at question %s." % channel_id)
       template_name = 'polls/detail.html'
       slack = SlackUtil()
       messages = slack.listMessages(channel_id)
       #print("messages in view", messages)
       channelMessages = []
       for key,value in messages.items():
           channelMessage = value
           channelMessages.append(channelMessage)
       channel_name = slack.getChannelById(channel_id)    
       context = {'messages': channelMessages,
                   'channel': channel_name}
       return render(request, template_name, context)

def results(request, user_id):

    template_name = 'polls/results.html'
    slack = SlackUtil()
    channels = slack.listChannels()
    messages = {}
    for channel in channels:
        #print("channel in view",channel)
        channelMessages = slack.listMessages(channel["id"])
        messages.update({channel["id"]:channelMessages})
    #print("in results", messages)    
    userMessages = slack.groupThreadMessagesByUser(messages)
    #print("in results userMessages", userMessages)
    nlp = NLPUtil()
    userSpecificMessages = {}
    #for key,value in userMessages.items():
    threadMessages = userMessages[user_id]
    for threadkey,threadMessage in threadMessages.items():
        for messageKey,message in threadMessage.items():
            userSpecificMessages.update({threadkey:message})
    print("in results userspecific",userSpecificMessages)
    sentiments = nlp.analyseContentSentiment(userSpecificMessages)
    #print("in results",sentiments)
    user_name = slack.getUserById(user_id)
    context = {'sentiments': sentiments,
               'user': user_name
               }
    return render(request, template_name, context)

def threads(request, thread_id):

    full_path = request.get_full_path()
    split_path = full_path.split("=")

    channel_id = split_path[-1]
    template_name = 'polls/threads.html'
    slack = SlackUtil()
    messages = slack.getRepliesByThreadId(channel_id,thread_id)
    
    threadMessages = {}
    for message in messages:
        threadMessages[message["ts"]]= message

    nlp = NLPUtil()
    
    #print("in threads userspecific",threadMessages)
    sentiments = nlp.analyseContentSentiment(threadMessages)
    #print("in results",sentiments)
    context = {'sentiments': sentiments,
               'thread': thread_id
               }
    return render(request, template_name, context)
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

# def detail(request, channel_id):
#      template = 'polls/detail.html'
#      slack = SlackUtil()
#      messages = slack.listMessages(channel_id)
#      context = {'messages': messages}
#      return render(request, template_name, context)


# def results(request, user_id):
#     template = 'polls/results.html'
# # context_object_name = 'messages'
#     slack = SlackUtil()
#     userMessages = slack.groupThreadMessagesByUser(user_id)
#.    nlp = NLPUtil()
#.    messages = nlp.analyzeContentSentiment(userMessages)
#     context = {'messages': messages,
#                  'user':user_id}

#     return render(request, template_name, context)
