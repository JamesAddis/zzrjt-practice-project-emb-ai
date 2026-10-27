''' Executing this function initiates the application of sentiment
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''

import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

import . from error_messages
import . from success_results

app = Flask("Sentiment Analyzer")
app.secret_key = str(os.environ['WTF_CSRF_SECRET_KEY'])
csrf = CSRFProtect(app)