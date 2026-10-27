''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''

from flask import render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer
from PracticeProject import app

import .constants as em
from .success_results import success_result_message

@app.route("/api/sentimentanalyzer")
def sent_analyzer():
    ''' This code receives the text from the HTML interface and 
        runs sentiment analysis over it using sentiment_analysis()
        function. The output returned shows the label and its confidence 
        score for the provided text.
    '''
    text_to_analyze = request.args.get("textToAnalyze")

    if text_to_analyze is None:
        return ({"message":em.TEXT_MISSING},400)
    if text_to_analyze.strip() == "":
        return ({"message":em.TEXT_EMPTY},422)
    if text_to_analyze.isdigit():
        return ({"message":em.TEXT_DIGIT},422)

    result = sentiment_analyzer(text_to_analyze)
    if result["label"] is None or result["score"] is None:
        return ({"message":em.AI_ISSUE},406)

    return success_result_message(result["label"],result["score"])