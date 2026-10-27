''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''

from flask import render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer
from PracticeProject import app
import .error_messages as em
from .success_results import success_result_message

@app.route("/", methods=["GET","POST"])
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
        POST response is used to provide no javascript method of using site's HTML form
    '''
    if request.method == "GET":
        return render_template("index.html")

    text_to_analyze = request.form.get("textToAnalyze")

    is_error=True
    text_result=""

    if text_to_analyze is None:
        text_result = em.TEXT_MISSING
    elif text_to_analyze.strip() == "":
        text_result = em.TEXT_EMPTY
    elif text_to_analyze.isdigit():
        text_result = em.TEXT_DIGIT
    else:
        result = sentiment_analyzer(text_to_analyze)
        if  result["label"] is None or result["score"] is None:
            text_result = em.AI_ISSUE
        else:
            text_result = success_result_message(result["label"], result["score"])
            is_error = False

    return render_template(
        "index.html",
        text_to_analyze=text_to_analyze,
        is_error=is_error,
        sentiment_analysis_result=text_result)
