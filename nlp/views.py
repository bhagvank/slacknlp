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
    login page call

    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
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
    page authentication
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """
    #slack = SlackUtil()
    #channels = slack.listChannels()
    print("authenticating")
    # messages = listMessages("CBR05AS5N")
    username = request.POST['useremail']
    password = request.POST['password']

    error_password = None
    try:
       user = get_object_or_404(SlackUser, username=username)
    except:
       template_name = 'nlp/login.html'
       error_username = "Invalid username"
       context = {'error_useremail': error_username,
                'error_password': error_password}
       return render(request, template_name,context)   
    #print(user)
    if user:
       check, error_username, error_password = user.authenticate(username, password)
       print(check,error_username,error_password)
       if check:

          template_name = 'nlp/main.html'
       else :
         print("setting template as login") 
         template_name = 'nlp/login.html'   
    else :
        print("setting template as login")
        template_name = 'nlp/login.html'
        error_username = "Invalid username"
    context = {'error_useremail': error_username,
                'error_password': error_password}
    # context_object_name = 'channels'
    return render(request, template_name,context)    


def main(request):
    """
    main page call

    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
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
    sign up page call
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """

    template_name = 'nlp/signup.html'
    #context = {'channels': channels}
    # context_object_name = 'channels'
    return render(request, template_name)    

def signin(request):
    """
    sign in - sign up processing
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """
    #slack = SlackUtil()
    #channels = slack.listChannels()
    #printf("signup")
    # messages = listMessages("CBR05AS5N")
    username = request.POST['useremail']
    password = request.POST['password']
    confirmPassword = request.POST['confirmPassword']
    print("password, confirmPassword",password,confirmPassword)

    #if confirmPassword == password:

    error_confirm_password = None
    error_username = None
    error_password = None
    #template_name = 'nlp/signup.html'

    error_username = _validate_username(username)
    error_password, error_confirm_password = _validate_password(password,confirmPassword)

    
    if error_username == None and error_password == None and error_confirm_password == None:
       if password == confirmPassword:
               #print("password is equal to confirmPassword") 
          user = SlackUser(username=username,password=password)
          user.save()   
          template_name = 'nlp/login.html'
       else :
               #error_confirm_password = "password and confirm password do not match"
          template_name = 'nlp/signup.html'
    else :
            #error_password = "password is not valid"
            #error_confirm_password = "confirm_password is not valid" 
            template_name = 'nlp/signup.html'     
      
    context = {'error_confirm_password': error_confirm_password,
                'error_useremail': error_username,
                'error_password': error_password 
                }
    # context_object_name = 'channels'
    return render(request, template_name,context)

def search(request):
    """
    sign in - sign up processing
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """
    #slack = SlackUtil()
    #channels = slack.listChannels()
    #printf("signup")
    # messages = listMessages("CBR05AS5N")
    search_text = request.POST['Search']
   
    #if confirmPassword == password:

    error_search = None
    
    #template_name = 'nlp/signup.html'

    error_search = _validate_search(search_text)
    
    messages = []
    
    if error_search == None:

          slack = SlackUtil()
          messages = slack.searchAll(search_text,1)
               #error_confirm_password = "password and confirm password do not match"
          template_name = 'nlp/search.html'
    else :
            #error_password = "password is not valid"
            #error_confirm_password = "confirm_password is not valid" 
            template_name = 'nlp/index.html'     
      
    context = { 'error_search': error_search,
                'query': search_text,
                'messages' : messages,
                'nextCursor': None
                }
    # context_object_name = 'channels'
    return render(request, template_name,context)     

def index(request):
    """
    index page

    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """
    #print("index")
    
    page,count = _parsePage(request)

    print("page", page)

    slack = SlackUtil()
    #channels = slack.listChannels()
    channels,nextCursor = slack.listChannelsPage(page,count)
    #printf("channels", channels)
    # messages = listMessages("CBR05AS5N")
    template_name = 'nlp/index.html'
    context = {'channels': channels,
                'nextCursor': nextCursor}
    # context_object_name = 'channels'
    return render(request, template_name, context)

def detail(request, channel_id):
       """
          detail page
         Parameters
         ----------
         request : HttpRequest
         request object

         Returns
          -----------
         HttpResponse
        content is the result of render method  

       """    

       #return HttpResponse("You're looking at question %s." % channel_id)
       page,count = _parsePage(request)

       
       slack = SlackUtil()
       #messages = slack.listMessages(channel_id)
       messages,nextCursor = slack.listMessagesPage(channel_id,page,count)
       #print("messages in view", messages)
       channelMessages = []
       for key,value in messages.items():
           channelMessage = value
           channelMessages.append(channelMessage)
       channel_name = slack.getChannelById(channel_id)

       template_name = 'nlp/detail.html'

       context = {'messages': channelMessages,
                   'channel': channel_name,
                   'channel_id': channel_id,
                   'nextCursor': nextCursor}
       return render(request, template_name, context)

def results(request, user_id):
    """
    results page
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """
    full_path = request.get_full_path()
    split_path = full_path.split("&")

    

    page = None

    channel_id = None

    if "&" in full_path:

       pagePath = split_path[-1].split("=")

       page = pagePath[-1]

       print("page ", page)

       previous_path = split_path[0].split("=")

       channel_id = previous_path[-1]

    else:
    
       split_path = full_path.split("=")
       channel_id = split_path[-1]


    count = 10


    template_name = 'nlp/results.html'
    slack = SlackUtil()
    #messages= {}
    messages, nextCursor = slack.getMessagesByUserPage(channel_id,user_id,page,count)
    channel_name = slack.getChannelById(channel_id)
    nlp = NLPUtil()

    sentiments = nlp.analyseContentSentiment(messages)
    #print("in results",sentiments)
    user_name = slack.getUserById(user_id)
    context = {'sentiments': sentiments,
               'user': user_name,
                'user_id':user_id,
                'channel_id':channel_id,
               'channel': channel_name,
               'nextCursor': nextCursor
               }
    return render(request, template_name, context)

def threads(request, thread_id):
    """
    threads page
    Parameters
    ----------
    request : HttpRequest
         request object

    Returns
    -----------
     HttpResponse
        content is the result of render method     
    """    


    full_path = request.get_full_path()
    split_path = full_path.split("&")

    

    page = None

    channel_id = None

    if "&" in full_path:

       pagePath = split_path[-1].split("=")

       page = pagePath[-1]

       print("page ", page)

       previous_path = split_path[0].split("=")

       channel_id = previous_path[-1]

    else:
    
       split_path = full_path.split("=")
       channel_id = split_path[-1]

    count = 10


    slack = SlackUtil()
    messages,nextCursor = slack.getRepliesByThreadIdPage(channel_id,thread_id,page,count)
    
    #threadMessages = {}
    #for message in messages:
    #    threadMessages[message["ts"]]= message

    nlp = NLPUtil()
    
    #print("in threads userspecific",threadMessages)
    sentiments = nlp.analyseContentSentiment(messages)

    channel = slack.getChannelById(channel_id)
    #print("in results",sentiments)
    context = {'sentiments': sentiments,
               'thread': thread_id,
                'channel': channel,
                'channel_id': channel_id,
                'nextCursor': nextCursor
               }
    template_name = 'nlp/threads.html' 
              
    return render(request, template_name, context)


def _parsePage(request):

    full_path = request.get_full_path()

    split_path = full_path.split("?")

    #print("split_path-1",split_path[-1])

    page = None

    if "?" in full_path:

       pagePath = split_path[1].split("page=")

       page = pagePath[-1]

    count = 10

    return page,count
def _validate_username(username):
    error_username = None    
    if username == None:
       #print("error in username")
       error_username = "user email is blank"
       #template_name = 'nlp/signup.html' 
    if "@" not in username or "." not in username :
       error_username = "user email is not valid" 
         #template_name = 'nlp/signup.html'       
    return error_username

def _validate_search(search):
    error_search = None    
    if search == None:
       error_search = "search query is blank"      
    return error_search

def _validate_password(password,confirm_password):
    error_password = None
    error_confirm_password = None
    if password == None:
       error_password = "password is blank"
    if confirm_password == None:
       error_confirm_password = "confirm password is blank"
    if password != None and confirm_password != None:
       if password == confirm_password:
          error_password = None
          error_confirm_password = None
       else :
          error_password = "password and confirm_password do not match"
          error_confirm_password = "password and confirm_password do not match"   
    return error_password, error_confirm_password      


   





