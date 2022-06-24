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
model = joblib.load("../models/model.sav")

app = Flask(__name__)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def hello_world():  # put application's code here
    return render_template('master.html')

# web page that handles user query and displays model results
@app.route('/auto-write', methods=['POST'])
def classify():
    prediction_values = [
        request.form['loan_limit'],
        request.form['pre_approval'],
        request.form['loan_type'],
        request.form['loan_purpose'],
        request.form['line_of_credit'],
        request.form['commercial_loan'],
        request.form['loan_amount'],
        request.form['interest_rate'],
        request.form['interest_rate_spread'],
        request.form['upfront_charges'],
        request.form['term'],
        request.form['negative_amortization'],
        request.form['interest_only'],
        request.form['lump_sum_payment'],
        request.form['property_value'],
        request.form['construction_type'],
        request.form['occupancy_type'],
        request.form['property_type'],
        request.form['units'],
        request.form['income'],
        request.form['credit_type'],
        request.form['credit_score'],
        request.form['co_borrower_credit_type'],
        request.form['application_taken'],
        request.form['ltv'],
        request.form['deposit_type'],
        request.form['dti'],
    ]

    columns = [
        'loan_limit',
        'pre_approval',
        'loan_type',
        'loan_purpose',
        'line_of_credit',
        'commercial_loan',
        'loan_amount',
        'interest_rate',
        'interest_rate_spread',
        'upfront_charges',
        'term',
        'negative_amortization',
        'interest_only',
        'lump_sum_payment',
        'property_value',
        'construction_type',
        'occupancy_type',
        'property_type',
        'units',
        'income',
        'credit_type',
        'credit_score',
        'co_borrower_credit_type',
        'application_taken',
        'ltv',
        'deposit_type',
        'dti',
    ]

    # use model to predict classification for query
    classification_labels = model.predict(prediction_values)[0]
    classification_results = dict(zip(columns, classification_labels))

    # This will render the results.html Please see that file.
    return render_template(
        'results.html',
        classification_result=classification_results
    )

def main():
    app.run(host='127.0.0.1', port=3000, debug=True)

if __name__ == '__main__':
    main()
