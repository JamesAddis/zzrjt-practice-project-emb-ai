"""
Sentiment Analysis functions using Watson
"""

import json
import requests
import config

# constants
DEFAULT_RESULT={"label":None, "score":None}

def sentiment_analyzer(text_to_analyse):
    """
    Sends request to watson ai API for emotion detection
    status 200: return label and score from document sentiment
    otherwise: return None for label and score
    """
    response = requests.post(
        config.WATSON_REQUEST_URL,
        json = { "raw_document": { "text": text_to_analyse } },
        headers=config.DEFAULT_WATSON_HEADER,
        timeout=config.DEFAULT_WATSON_TIMEOUT)

    print (response.status_code)
    print(response.text)

    if response.status_code == 200:
        formatted_response = json.loads(response.text)
        label = formatted_response['documentSentiment']['label']
        score = formatted_response['documentSentiment']['score']
        return {"label":label, "score":score}

    return DEFAULT_RESULT
