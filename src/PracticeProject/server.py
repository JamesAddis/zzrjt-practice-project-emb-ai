''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''

from flask import render_template, request
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer
from PracticeProject import app

# constants
TEXT_MISSING="Text is required"
TEXT_EMPTY="Text is required, cannot be an empty string"
TEXT_DIGIT="Text cannot be only digit/numerical value"
WATSON_ISSUE="Invalid input ! Try again"
RESULT_STR="The given text has been identified as {} with a score of {}"

@app.route("/api/sentimentAnalyzer")
def sent_analyzer():
    ''' This code receives the text from the HTML interface and 
        runs sentiment analysis over it using sentiment_analysis()
        function. The output returned shows the label and its confidence 
        score for the provided text.
    '''
    text_to_analyze = request.args.get("textToAnalyze")

    if text_to_analyze is None:
        return ({"message":TEXT_MISSING},400)
    if text_to_analyze.strip() == "":
        return ({"message":TEXT_EMPTY},422)
    if text_to_analyze.isdigit():
        return ({"message":TEXT_DIGIT},422)

    result = sentiment_analyzer(text_to_analyze)
    if result["label"] is None or result["score"] is None:
        return ({"message":WATSON_ISSUE},406)

    return RESULT_STR.format(result["label"],result["score"])

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
        text_result =TEXT_MISSING
    elif text_to_analyze.strip() == "":
        text_result =TEXT_EMPTY
    elif text_to_analyze.isdigit():
        text_result =TEXT_DIGIT
    else:

        result = sentiment_analyzer(text_to_analyze)
        if  result["label"] is None or result["score"] is None:
            text_result = WATSON_ISSUE
        else:
            text_result = RESULT_STR.format(result["label"],result["score"])
            is_error = False

    return render_template(
        "index.html",
        text_to_analyze=text_to_analyze,
        is_error=is_error,
        sentiment_analysis_result=text_result)
