from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import loader
from .models import SlackUser
from .slackutils import SlackUtil
from .NLPUtils import NLPUtil

def login(request):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    #slack = SlackUtil()
    #channels = slack.listChannels()
    #printf("channels", channels)
    # messages = listMessages("CBR05AS5N")
    template_name = 'nlp/login.html'
    #context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name)

def authenticate(request):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    #slack = SlackUtil()
    #channels = slack.listChannels()
    #printf("channels", channels)
    # messages = listMessages("CBR05AS5N")
    username = request.POST['useremail']
    password = request.POST['password']

    user = get_object_or_404(SlackUser, username=username)

    if user.authenticate(username,password):

       template_name = 'nlp/main.html'
    else :
    
       template_name = 'nlp/login.html'   
    #context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name)    


def main(request):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    #slack = SlackUtil()
    #channels = slack.listChannels()
    #printf("channels", channels)
    # messages = listMessages("CBR05AS5N")
    template_name = 'nlp/main.html'
    #context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name)    

def signup(request):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """

    template_name = 'nlp/signup.html'
    #context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name)    

def signin(request):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    #slack = SlackUtil()
    #channels = slack.listChannels()
    #printf("signup")
    # messages = listMessages("CBR05AS5N")
    username = request.POST['useremail']
    password = request.POST['password']
    confirmPassword = request.POST['confirmPassword']
    print("password, confirmPassword",password,confirmPassword)

    if password == confirmPassword:
       user = SlackUser(username=username,password=password)
       user.save()   
       template_name = 'nlp/login.html'
    else :
       template_name = 'nlp/signup.html'   
    #context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name) 

def index(request):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    print("index")
    slack = SlackUtil()
    channels = slack.listChannels()
    #printf("channels", channels)
    # messages = listMessages("CBR05AS5N")
    template_name = 'nlp/index.html'
    context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name, context)

def detail(request, channel_id):
    #return HttpResponse("You're looking at question %s." % channel_id)
       template_name = 'nlp/detail.html'
       slack = SlackUtil()
       messages = slack.listMessages(channel_id)
       #print("messages in view", messages)
       channelMessages = []
       for key,value in messages.items():
           channelMessage = value
           channelMessages.append(channelMessage)
       channel_name = slack.getChannelById(channel_id)


       context = {'messages': channelMessages,
                   'channel': channel_name,
                   'channel_id': channel_id}
       return render(request, template_name, context)

def results(request, user_id):

    full_path = request.get_full_path()
    split_path = full_path.split("=")

    channel_id = split_path[-1]

    template_name = 'nlp/results.html'
    slack = SlackUtil()
    #messages= {}
    messages = slack.getMessagesByUser(channel_id,user_id)
    channel_name = slack.getChannelById(channel_id)
    #channels = slack.listChannels()
    #messages = {}
    #for channel in channels:
        #print("channel in view",channel)
    #   channelMessages = slack.listMessages(channel["id"])
    #    messages.update({channel["id"]:channelMessages})
    #print("in results", messages)    
    threadMessages = slack.groupThreadMessagesByUser(messages)
    #print("in results userMessages", userMessages)
    nlp = NLPUtil()
    #userSpecificMessages = {}
    #for key,value in userMessages.items():
    #threadMessages = userMessages[user_id]
    #for threadkey,threadMessage in threadMessages.items():
    #    for messageKey,message in threadMessage.items():
    #        userSpecificMessages.update({threadkey:message})
    #print("in results userspecific",userSpecificMessages)
    allMessages = {}
    for key,threadMessage in threadMessages.items():
        for messagekey, message in threadMessage.items():
            allMessages.update({messagekey:message})
    sentiments = nlp.analyseContentSentiment(allMessages)
    #print("in results",sentiments)
    user_name = slack.getUserById(user_id)
    context = {'sentiments': sentiments,
               'user': user_name,
               'channel': channel_name
               }
    return render(request, template_name, context)

def threads(request, thread_id):

    full_path = request.get_full_path()
    split_path = full_path.split("=")

    channel_id = split_path[-1]
    template_name = 'nlp/threads.html'
    slack = SlackUtil()
    messages = slack.getRepliesByThreadId(channel_id,thread_id)
    
    threadMessages = {}
    for message in messages:
        threadMessages[message["ts"]]= message

    nlp = NLPUtil()
    
    #print("in threads userspecific",threadMessages)
    sentiments = nlp.analyseContentSentiment(threadMessages)

    channel = slack.getChannelById(channel_id)
    #print("in results",sentiments)
    context = {'sentiments': sentiments,
               'thread': thread_id,
                'channel_id': channel
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
