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

        note = f"have an upfront charge of {self.request.form['upfront_charges']}"

        series = self.dataset[self.dataset['upfront_charges'] == 10.25]['upfront_charges'].value_counts(normalize=True)

        percentage = 0

        if series.empty or series[0] == 0:
            note = f"{percentage}% of {self.status_text} {note}"

            return note

        

    def binary_distribution_percentage(self, form_field):
        percentage = np.round(self.dataset[self.dataset['status'] == self.status][form_field].value_counts(normalize=True)[
                     int(self.request.form[form_field])] * 100, 2)

        return percentage
