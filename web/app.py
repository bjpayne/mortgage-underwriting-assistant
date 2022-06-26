import joblib
import re
import numpy as np
import pandas as pd

from flask import Flask, render_template, request
from datetime import datetime
from web.providers.ResultsProvider import ResultsProvider

# Load model
model = joblib.load("../models/model.sav")

# Instantiate app
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
        'int': int,
        'status': status,
        'form_data': request.form,
        'dataset': dataset,
        'plot_data': dataset.to_json(),
        'pre_approval_notes': results_provider.pre_approval_notes(),
        'line_of_credit_notes': results_provider.line_of_credit_notes(),
        'negative_amortization_notes': results_provider.negative_amortization_notes(),
        'upfront_charges_notes': results_provider.upfront_charges_notes(),
        'upfront_charges_data': results_provider.upfront_charges_data(),
        'interest_only_notes': results_provider.interest_only_notes(),
        'income_notes': results_provider.income_notes(),
        'income_data': results_provider.income_data(),
        'credit_score_notes': results_provider.credit_score_notes(),
        'credit_score_data': results_provider.credit_score_data(),
        'property_value_notes': results_provider.property_value_notes(),
        'property_value_data': results_provider.property_value_data(),
        'loan_amount_notes': results_provider.loan_amount_notes(),
        'loan_amount_data': results_provider.loan_amount_data(),
        'ltv_notes': results_provider.ltv_notes(),
        'ltv_data': results_provider.ltv_data(),
    }

    # This will render the results.html Please see that file.
    return render_template('results.html', **template_data)


def main():
    app.run(threaded=True, port=5000)


if __name__ == '__main__':
    main()
