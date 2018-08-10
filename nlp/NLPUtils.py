from google.cloud import language
from google.oauth2 import service_account
from google.cloud.language import enums
from google.cloud.language import types
from django.conf import settings
from boto.s3.connection import S3Connection
import os

import json

class NLPUtil:

    def __init__(self):

        self.data = []


    def analyseContentSentiment(self, messages):
        #s3 = S3Connection(os.environ['ACCESS_KEY_ID'], os.environ['SECRET_ACCESS_KEY'])
        #s3.Bucket('googleservicejson').download_file('/app/service.json', 'service.json')
        credentials = service_account.Credentials.from_service_account_file(os.environ['GOOGLE_SERVICE']
        )

        messageSentiments = []
        #print("messages analyse",messages)
        for key, value in messages.items():
            message = value
            client = language.LanguageServiceClient(credentials=credentials,)
            document = language.types.Document(
            content=message["text"],
            language='en',
            type=enums.Document.Type.PLAIN_TEXT,

             )
            response = client.analyze_sentiment(
             document=document, encoding_type='UTF8',)
            sentiment = response.document_sentiment
            userMessage = {}
            #userMessage["thread_ts"] = key
            userMessage["message"] = message
            userMessage["score"] = sentiment.score
            userMessage["magnitude"] = sentiment.magnitude
            messageSentiments.append(userMessage)
        # messageSentiments.append(sentiment)
        return messageSentiments




