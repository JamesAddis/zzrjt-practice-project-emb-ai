''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''

import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask("Sentiment Analyzer")
app.secret_key = str(os.environ['WTF_CSRF_SECRET_KEY'])
csrf = CSRFProtect(app)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
