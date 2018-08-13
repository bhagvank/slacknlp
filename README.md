# slacknlp
converse and learn adaptively

![alt text](https://floating-crag-10115.herokuapp.com/static/nlp/images/logo.jpg)

* [SlackNLP Demo](https://floating-crag-10115.herokuapp.com/nlp/)

Video content management, AI, Blockchain and Virtual/Augmented reality technologies are changing the learning management platforms. Customer focused learning systems are emerging in enterprises. Enterprises are structuring their curriculum products to help solve the high value use cases of their customers. Members of the LMS system can tailor their educational experience by choosing courses based on their learning styles. The courses are becoming more effective and helping members retain information. Platforms are differentiating by providing better, faster ways to find relevant content, whenever and wherever learners need it. Modern learning management platform is an end-to-end eLearning solution which has capabilities to create, distribute, edit and manage entire courses from start to finish independent of the content. Educational success and fulfilment are achieved through personalization and optimization of the learner’s path through courses and gaining of competencies. This new class of learning technology vendors is making it possible to augment their systems with cloud-based applications which can be easily integrated with an enterprise-scale technology ecosystem. Enterprises are now tracking and analyzing learning experiences with incredible precision which can be used to improve ongoing program and business outcomes. Tracking and reporting comes in learner-oriented dashboards and reports built for the staff. 

AI based NLP engine scans and parses the messages from Slack. Slack is used for communicating new courses, mentor conversations, cohort groups, general discussions and other posting from students. NLP engine has the capability of identifying threads and conversations. This will help to know and analyse  the sentiments, tone, mood,emotions, utterances and other parameters  from the conversations. This will help in using the historical data about the students and their preferences to adapt the learning path and course content.   Adaptive Learning is used to change the ongoing content of materials and assessments  based on the educational goals. NLP engine helps in capturing time to mastery, completion rates, material reading complexity, language complexity and complexity of content topics. These areas are important for historical data which will be used for adaptive learning.

# Instructions for setting up locally
1. Ensure that postgres is installed, python3 and django for polls app - mysite folder.

  * [Python3](https://www.python.org/downloads/)

  * [Django](https://docs.djangoproject.com/en/2.0/topics/install/#installing-official-release)

  * [Postgres](https://elements.heroku.com/addons/heroku-postgresql)
  
  
2.git clone this repository
```
git clone https://github.com/bhagvank/slacknlp.git

```

3. create slack api token and google service accounts

   * [Slack](https://api.slack.com/custom-integrations/legacy-tokens)
   * [Google](https://cloud.google.com/compute/docs/access/service-accounts)
   
4. run locally using settings
```
python manage.py runserver --settings=mysite.run_settings

```
  

# Instructions for setting up on heroku



  
  * Slack NLP
## Prerequisites

1. Ensure that postgres is installed, python3 and django for polls app - mysite folder.

  * [Python3](https://www.python.org/downloads/)

  * [Django](https://docs.djangoproject.com/en/2.0/topics/install/#installing-official-release)

  * [Postgres](https://elements.heroku.com/addons/heroku-postgresql)
  
  * [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)

2.git clone this repository
```
git clone https://github.com/bhagvank/slacknlp.git

```

3. create slack api token and google service accounts

   * [Slack](https://api.slack.com/custom-integrations/legacy-tokens)
   * [Google](https://cloud.google.com/compute/docs/access/service-accounts)

4.create account on heroku
```
heroku login 

heroku create

git push heroku master

heroku open
```

5. updated config vars on Heroku and upload service.json to S3

  * [Heroku](https://devcenter.heroku.com/articles/config-vars)
  * [AmazonS3](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html)
  
## Slack NLP  - with Postgres

1.Create user from the command line
```
heroku run python manage.py createsuperuser
```

3.run migrations
```
heroku run python manage.py migrate

```
4.run the server
```
heroku run python manage.py runserver
```
5. check the logs on heroku
```
heroku logs --tail
```


