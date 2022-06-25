import joblib
import re
import numpy as np
import pandas as pd

from flask import Flask
from flask import render_template, request, jsonify
from datetime import datetime
from providers.ResultsProvider import ResultsProvider

# load model
model = joblib.load("../models/model.sav")

app = Flask(__name__)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


# main page
@app.route('/')
def index():
    return render_template('index.html')

# web page that handles user query and displays model results
@app.route('/auto-write', methods=['POST'])
def auto_write():
    prediction_values = [
        request.form['loan_limit'],
        request.form['pre_approval'],
        request.form['loan_type'],
        request.form['loan_purpose'],
        request.form['line_of_credit'],
        request.form['commercial_loan'],
        re.sub('[^0-9.]', '', request.form['loan_amount']),
        request.form['interest_rate'],
        request.form['interest_rate_spread'],
        re.sub('[^0-9.]', '', request.form['upfront_charges']),
        request.form['term'],
        request.form['negative_amortization'],
        request.form['interest_only'],
        request.form['lump_sum_payment'],
        re.sub('[^0-9.]', '', request.form['property_value']),
        request.form['construction_type'],
        request.form['occupancy_type'],
        request.form['property_type'],
        request.form['units'],
        re.sub('[^0-9.]', '', request.form['income']),
        request.form['credit_type'],
        request.form['credit_score'],
        request.form['co_borrower_credit_type'],
        request.form['application_taken'],
        request.form['ltv'],
        request.form['deposit_type'],
        request.form['dti'],
    ]

    # use model to predict classification for query
    status = model.predict(np.array(prediction_values).reshape(1, -1))[0]

    # load the cleaned data for results plots
    dataset = pd.read_csv('../data/processed_data.csv')

    results_provider = ResultsProvider(dataset, status, request)

    template_data = {
        'status': status,
        'form_data': request.form,
        'dataset': dataset,
        'plot_data': dataset.to_json(),
        'pre_approval_notes': results_provider.pre_approval_notes(),
        'line_of_credit_notes': results_provider.line_of_credit_notes(),
        'negative_amortization_notes': results_provider.negative_amortization_notes()
    }

    # This will render the results.html Please see that file.
    return render_template('results.html', **template_data)


def pre_approval_notes(dataset, status, request):
    status_text = "approved" if status == 1 else "denied"

    pre_approval_text = "are pre approved" if request.form['pre_approval'] == 1 else "are not pre approved"

    percentage = np.round(dataset[dataset['status'] == status]['pre_approval'].value_counts(normalize=True)[int(request.form['pre_approval'])] * 100, 2)

    note = f"{percentage}% of {status_text} files {pre_approval_text}"

    return note


def line_of_credit_notes(dataset, status, request):
    status_text = "approved" if status == 1 else "denied"

    line_of_credit_text = "are a line of credit" if request.form['line_of_credit'] == 1 else "are not a line of credit"

    percentage = np.round(dataset[dataset['status'] == status]['line_of_credit'].value_counts(normalize=True)[int(request.form['line_of_credit'])] * 100, 2)

    note = f"{percentage}% of {status_text} files {line_of_credit_text}"

    return note

def main():
    app.run(host='127.0.0.1', port=3000, debug=True)


if __name__ == '__main__':
    main()
