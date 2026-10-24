"""
Sentiment Analysis functions
"""

import json
import requests

# constants
REQUEST_URL = "https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict" # pylint: disable=line-too-long
DEFAULT_HEADER = {
    "grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
DEFAULT_RESULT={"label":None, "score":None}

def sentiment_analyzer(text_to_analyse):
    """
    Sends request to watson ai API for emotion detection
    """
    response = requests.post(
        REQUEST_URL,
        json = { "raw_document": { "text": text_to_analyse } },
        headers=DEFAULT_HEADER,
        timeout=120)

    print (response.status_code)
    print(response.text)

    if response.status_code == 200:
        formatted_response = json.loads(response.text)
        label = formatted_response['documentSentiment']['label']
        score = formatted_response['documentSentiment']['score']
        return {"label":label, "score":score}

    return DEFAULT_RESULT
