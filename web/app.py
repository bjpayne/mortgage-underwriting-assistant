import joblib
import re
import numpy as np

from flask import Flask
from flask import render_template, request, jsonify
from datetime import datetime

# load model
model = joblib.load("../models/model.sav")

app = Flask(__name__)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


# main page
@app.route('/')
def index():
    return render_template('master.html')

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
    status = model.predict(np.array(prediction_values).reshape(1, -1))

    # This will render the results.html Please see that file.
    return render_template('results.html', status=status, form_data=request.form)


def main():
    app.run(host='127.0.0.1', port=3000, debug=True)


if __name__ == '__main__':
    main()
