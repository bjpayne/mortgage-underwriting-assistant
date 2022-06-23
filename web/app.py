import json
import plotly
import sqlite3
import joblib
import pandas as pd

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Pie
from datetime import datetime

# load model
# model = joblib.load("../models/model.sav")

app = Flask(__name__)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def hello_world():  # put application's code here
    return render_template('master.html')

# web page that handles user query and displays model results
# @app.route('/classify')
# def classify():
#     # save user input in query
#     query = request.args.get('query', '')
#
#     # use model to predict classification for query
#     classification_labels = model.predict([query])[0]
#     classification_results = dict(zip(df.columns[4:], classification_labels))
#
#     # This will render the results.html Please see that file.
#     return render_template(
#         'results.html',
#         query=query,
#         classification_result=classification_results
#     )

def main():
    app.run(host='127.0.0.1', port=3000, debug=True)

if __name__ == '__main__':
    main()
