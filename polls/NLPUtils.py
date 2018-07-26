from google.cloud import language
from google.oauth2 import service_account
from google.cloud.language import enums
from google.cloud.language import types

import json

class NLPUtil:

    def __init__(self):

        self.data = []


    def analyseContentSentiment(self, messages):
        credentials = service_account.Credentials.from_service_account_file(
        'SlackNLP-07f85cf58b4e.json')

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
            userMessage["thread_ts"] = key
            userMessage["message"] = message
            userMessage["score"] = sentiment.score
            userMessage["magnitude"] = sentiment.magnitude
            messageSentiments.append(userMessage)
        # messageSentiments.append(sentiment)
        return messageSentiments




