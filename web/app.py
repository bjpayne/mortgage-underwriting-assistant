import os
import joblib
import re
import numpy as np
import pandas as pd

from flask import Flask, render_template, request
from datetime import datetime
from web.providers.ResultsProvider import ResultsProvider

# Set the web root directory
WEB_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model
model = joblib.load(f"{WEB_ROOT_DIR}/../models/model.sav")

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
        float(request.form['loan_limit']),
        int(request.form['pre_approval']),
        int(request.form['loan_type']),
        int(request.form['loan_purpose']),
        int(request.form['line_of_credit']),
        int(request.form['commercial_loan']),
        float(re.sub('[^0-9.]', '', request.form['loan_amount'])),
        float(request.form['interest_rate']),
        float(request.form['interest_rate_spread']),
        float(re.sub('[^0-9.]', '', request.form['upfront_charges'])),
        int(request.form['term']),
        int(request.form['negative_amortization']),
        int(request.form['interest_only']),
        int(request.form['lump_sum_payment']),
        float(re.sub('[^0-9.]', '', request.form['property_value'])),
        int(request.form['construction_type']),
        int(request.form['occupancy_type']),
        int(request.form['property_type']),
        int(request.form['units']),
        float(re.sub('[^0-9.]', '', request.form['income'])),
        int(request.form['credit_type']),
        int(request.form['credit_score']),
        int(request.form['co_borrower_credit_type']),
        int(request.form['application_taken']),
        float(request.form['ltv']),
        int(request.form['deposit_type']),
        float(request.form['dti']),
    ]

    # use model to predict classification for query
    status = model.predict(np.array(prediction_values).astype(float).reshape(1, -1))[0]

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


if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=True)
