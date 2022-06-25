import re
import numpy as np


class ResultsProvider:
    def __init__(self, dataset, status, request):
        self.dataset = dataset
        self.status = status
        self.request = request
        self.status_text = "approved" if self.status == 1 else "denied"

    def pre_approval_notes(self):
        note = "are pre approved" if self.request.form['pre_approval'] == 1 else "are not pre approved"

        percentage = self.binary_distribution_percentage('pre_approval')

        note = f"{percentage}% of {self.status_text} files {note}"

        return note

    def line_of_credit_notes(self):
        note = "are a line of credit" if self.request.form['line_of_credit'] == 1 else "are not a line of credit"

        percentage = self.binary_distribution_percentage('line_of_credit')

        note = f"{percentage}% of {self.status_text} files {note}"

        return note

    def negative_amortization_notes(self):
        note = "have negative amortization" if self.request.form['negative_amortization'] == 1 else \
            "do not have negative amortization"

        percentage = self.binary_distribution_percentage('negative_amortization')

        note = f"{percentage}% of {self.status_text} files {note}"

        return note

    def upfront_charges_notes(self):
        upfront_charges = float(re.sub('[^0-9.]', '', self.request.form['upfront_charges']))

        note = f" applications have an upfront charge of {self.request.form['upfront_charges']}"

        series = self.dataset[(self.dataset['status'] == self.status) &
                              (self.dataset['upfront_charges'] == upfront_charges)]['upfront_charges'] \
            .value_counts(normalize=True)

        if series.empty or series[0] == 0:
            return f"0% of {self.status_text} {note}"

        percentage = (series[upfront_charges] / self.dataset[(self.dataset['status'] == self.status)]['upfront_charges']
                      .shape[0]) * 100

        percentage = np.round(percentage, 4)

        note = f"{percentage}% of {self.status_text} {note}"

        return note

    def upfront_charges_data(self):
        bins = range(0, int(self.dataset[self.dataset['status'] == self.status]['upfront_charges'].max()), 2500)

        data = {
            'x': [*bins],
            'y': self.dataset[self.dataset['status'] == self.status]['upfront_charges'].value_counts(bins=bins)
                .to_list(),
        }

        return data

    def interest_only_notes(self):
        note = "are interest only" if self.request.form['interest_only'] == 1 else \
            "are not interest only"

        percentage = self.binary_distribution_percentage('interest_only')

        note = f"{percentage}% of {self.status_text} files {note}"

        return note

    def income_notes(self):
        income = float(re.sub('[^0-9.]', '', self.request.form['income']))

        note = f" applicants have an income of {self.request.form['income']}"

        series = self.dataset[(self.dataset['status'] == self.status) &
                              (self.dataset['income'] == income)]['income'] \
            .value_counts(normalize=True)

        if series.empty or series[0] == 0:
            return f"0% of {self.status_text} {note}"

        percentage = (series[income] / self.dataset[(self.dataset['status'] == self.status)]['income']
                      .shape[0]) * 100

        percentage = np.round(percentage, 4)

        note = f"{percentage}% of {self.status_text} {note}"

        return note

    def income_data(self):
        bins = range(0, int(self.dataset[self.dataset['status'] == self.status]['income'].max()), 2500)

        data = {
            'x': [*bins],
            'y': self.dataset[self.dataset['status'] == self.status]['income'].value_counts(bins=bins)
                .to_list(),
        }

        return data

    def credit_score_notes(self):
        credit_score = int(self.request.form['credit_score'])

        percentage = self.dataset[(self.dataset['status'] == self.status) &
                                  (self.dataset['credit_score'] == credit_score)]['credit_score'].shape[0] / \
                     self.dataset[self.dataset['status'] == self.status]['credit_score'].shape[0]

        percentage = np.round(percentage * 100, 2)

        note = f"{percentage}% of applicants have a credit score of {credit_score}"

        return note

    def credit_score_data(self):
        data = {
            'x': self.dataset[self.dataset['status'] == self.status]['credit_score'].unique().tolist(),
            'y': self.dataset[self.dataset['status'] == self.status]['credit_score'].value_counts().to_list()
        }

        return data

    def binary_distribution_percentage(self, form_field):
        percentage = np.round(
            self.dataset[self.dataset['status'] == self.status][form_field].value_counts(normalize=True)[
                int(self.request.form[form_field])] * 100, 2)

        return percentage
