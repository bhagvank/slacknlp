from django.urls import path

from . import views


#app_name = 'polls'
urlpatterns = [
   
    #path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'), 
    path('<channel_id>/', views.detail, name='detail'), 
    path('results/<user_id>/', views.results, name='results'),
    path('threads/<thread_id>/', views.threads, name='threads'),  
    # ex: /polls/5/
    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]