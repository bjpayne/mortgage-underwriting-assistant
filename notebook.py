# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13u_n64c0Dni4bf-QIaSBL5Goa5BJJ_Wd

# Mortgage Underwriting AI Assistant: Data Analysis

### Table of Contents

1. [Notebook setup](#Notebook-setup)
2. [ETL](#ETL)<br>
    2.1. [Year](#Year)<br>
    2.2. [Loan Limit](#Loan-limit)<br>
    2.3. [PreApproval](#PreApproval)<br>
    2.4. [Loan type](#Loan-type)<br>
    2.5. [Loan purpose](#Loan-purpose)<br>
    2.6. [Credit worthiness](#Credit-worthiness)<br>
    2.7. [Line of Credit](#Line-of-Credit)<br>
    2.8. [Commercial loan](#Commercial-loan)<br>
    2.9. [Loan amount](#Loan-amount)<br>
    2.10. [Interest rate](#Interest-rate)<br>
    2.11. [Interest rate spread](#Interest-rate-spread)<br>
    2.12. [Upfront charges](#Upfront-charges)<br>
    2.13. [Term](#Term)<br>
    2.14. [Negative ammortization](#Negative-ammortization)<br>
    2.15. [Interest only](#Interest-only)<br>
    2.16. [Lump sum payment](#Lump-sum-payment)<br>
    2.17. [Property value](#Property-value)<br>
    2.18. [Construction type](#Construction-type)<br>
    2.19. [Occupancy type](#Occupancy-type)<br>
    2.20. [Property type](#Property-type)<br>
    2.21. [Units](#Units)<br>
    2.22. [Income](#Income)<br>
    2.23. [Credit type](#Credit-type)<br>
    2.24. [CoBorrower credit type](#CoBorrower-credit-type)<br>
    2.25. [Age](#Age)<br>
    2.26. [Application taken](#Application-taken)<br>
    2.27. [LTV](#LTV)<br>
    2.28. [Deposit type](#Deposit-type)<br>
    2.29. [Status](#Status)<br>
3. [Fair Credit](#Fair-credit)<br>
4. [Build Model](#Model)<br>
5. [Evaluate Model](#Evaluate-model)<br>

### Notebook setup
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import ParameterGrid, StratifiedKFold

# %matplotlib inline

dataset = pd.read_csv('data.csv')

dataset.head()

"""Clean up column names"""

dataset.columns= dataset.columns.str.lower()

dataset.info()

"""### ETL

There are 34 features in the dataset. Analyze each feature setting the correct datatype, imputing missing values as needed and dropping features as needed

#### ID

ID can be dropped...status will be the independent feature
"""

dataset.drop('id', inplace=True, axis=1)

dataset.head()

"""#### Year"""

dataset['year'].unique()

"""All values in the year column are for 2019. This column can be dropped."""

dataset.drop('year', inplace=True, axis=1)

dataset.head()

"""#### Loan limit"""

dataset['loan_limit'].unique()

"""There are some NaN values in this vector that will need to be cleaned up."""

# Get a count of the number of applications missing the loan limits
dataset[dataset['loan_limit'].isnull()].shape[0]

"""3344 applications are missing a loan limit designation"""

dataset['loan_limit'].fillna(0, inplace=True)

dataset['loan_limit'].unique()

"""Encode conforming and non-conforming limits to 1 and 2"""

dataset['loan_limit'].replace({'cf': 1, 'ncf': 2}, inplace=True)

dataset['loan_limit'].unique()

"""#### PreApproval

Rename approv_in_adv to pre_approval
"""

dataset.rename(columns={"approv_in_adv": "pre_approval"}, inplace=True)

dataset['pre_approval'].unique()

"""Encode nopre and nan to 0, pre to 1"""

dataset['pre_approval'].fillna(0, inplace=True)

dataset['pre_approval'].replace({'nopre': 0, 'pre': 1}, inplace=True)

dataset['pre_approval'].unique()

"""#### Loan type"""

dataset['loan_type'].unique()

"""Drop the 'type' prefix, cast to int64"""

dataset['loan_type'] = dataset['loan_type'].str.replace('type', '').astype(np.int64)

dataset['loan_type'].unique()

"""#### Loan purpose"""

dataset['loan_purpose'].unique()

"""Replace NaN with p0 then drop the 'p' prefix then cast as Int64"""

dataset['loan_purpose'].fillna('p0', inplace=True)

dataset['loan_purpose'].unique()

dataset['loan_purpose'] = dataset['loan_purpose'].str.replace('p', '').astype(np.int64)

dataset['loan_purpose'].unique()

"""#### Credit worthiness"""

dataset['credit_worthiness'].unique()

"""Asses the correlation between credit worthiness and mortgage status"""

credit_worthiness_df = pd.DataFrame(dataset[['credit_worthiness', 'status']])

# dataset['pre_approval'].replace({'nopre': 0, 'pre': 1}, inplace=True)
credit_worthiness_df['credit_worthiness'].replace({'l1': 0, 'l2': 2}, inplace=True)

credit_worthiness_df.head()

plt.figure(figsize=(30, 20), dpi=100) 
_ = sns.heatmap(credit_worthiness_df.corr(), annot=True, annot_kws={"fontsize":12}, linecolor='white', \
            linewidth=1, fmt='.3f', cmap="viridis", cbar=False)

"""There doesn't appear to be a strong correlation between the credit worthiness field and the independent variable. Drop the credit worthiness column."""

dataset.drop(columns=['credit_worthiness'], inplace=True)

"""#### Line of Credit

Rename 'open_credit' to 'line_of_credit'
"""

dataset.rename(columns={'open_credit': 'line_of_credit'}, inplace=True)

dataset['line_of_credit'].unique()

"""Map nopc to 0 and opc to 1...cast to int64"""

dataset['line_of_credit'].replace({'nopc': 0, 'opc': 1}, inplace=True)

"""#### Commercial loan

Rename business_or_commercial to commercial_loan
"""

dataset.rename(columns={'business_or_commercial': 'commercial_loan'}, inplace=True)

dataset['commercial_loan'].unique()

"""Convert nob/c to 0 and b/c to 1"""

dataset['commercial_loan'].replace({'nob/c': 0, 'b/c': 1}, inplace=True)

"""#### Loan amount"""

dataset['loan_amount'].unique()

dataset['loan_amount'].isna().sum()

"""#### Interest rate"""

dataset['rate_of_interest'].unique()

"""Impute NaNs to 0.0"""

dataset['rate_of_interest'].unique()

dataset['rate_of_interest'].fillna(0.0, inplace=True)

dataset['rate_of_interest'].unique()

"""Rename rate_of_interest to interest_rate"""

dataset.rename(columns={'rate_of_interest': 'interest_rate'}, inplace=True)

"""#### Interest rate spread

Impute NaNs to 0.0
"""

dataset['interest_rate_spread'].fillna(0.0, inplace=True)

"""#### Upfront charges"""

dataset['upfront_charges'].unique()

"""Impute NaNs to 0.0"""

dataset['upfront_charges'].fillna(0.0, inplace=True)

dataset['upfront_charges'].unique()

"""#### Term"""

dataset['term'].unique()

"""Imput NaNs to 0. Conver to int64"""

dataset['term'] = dataset['term'].fillna(0).astype(np.int64)

dataset['term'].unique()

"""#### Negative ammortization"""

dataset['neg_ammortization'].unique()

"""Imput NaNs to 0s, convert not_neg to 0 and neg_amm to 1. Rename column to negative_ammortization"""

dataset['neg_ammortization'].fillna(0, inplace=True)

dataset['neg_ammortization'].replace({'not_neg': 0, 'neg_amm': 1}, inplace=True)

dataset.rename(columns={'neg_ammortization': 'negative_ammortization'}, inplace=True)

dataset['negative_ammortization'].unique()

"""#### Interest only"""

dataset['interest_only'].unique()

"""Convert not_int to 0, int_only to 1"""

dataset['interest_only'].replace({'not_int': 0, 'int_only': 1}, inplace=True)

dataset['interest_only'].unique()

"""#### Lump sum payment"""

dataset['lump_sum_payment'].unique()

"""Convert not_lpsm to 0, lpsm to 1"""

dataset['lump_sum_payment'].replace({'not_lpsm': 0, 'lpsm': 1}, inplace=True)

dataset['lump_sum_payment'].unique()

"""#### Property value"""

dataset['property_value'].isna().sum()

"""Impute NaNs to 0.0"""

dataset['property_value'].fillna(0.0, inplace=True)

dataset['property_value'].isna().sum()

"""#### Construction type"""

dataset['construction_type'].unique()

"""Convert single borrower to 1, multi-home to 2...impute NaNs to 0"""

dataset['construction_type'].fillna(0, inplace=True)

dataset['construction_type'].replace({'sb': 1, 'mh': 2}, inplace=True)

dataset['construction_type'].unique()

"""#### Occupancy type"""

dataset['occupancy_type'].unique()

"""Convert primary residence (pr) to 1, secondary residence (sr) to 2, investment property (ir) to 3...impute NaNs to 0"""

dataset['occupancy_type'].fillna(0, inplace=True)

dataset['occupancy_type'].replace({'pr': 1, 'sr': 2, 'ir': 3}, inplace=True)

dataset['occupancy_type'].unique()

"""#### Property type

Rename secured_by to property_type
"""

dataset.rename(columns={'secured_by': 'property_type'}, inplace=True)

dataset['property_type'].unique()

"""Convert home to 1, land to 2...impute NaNs to 0"""

dataset['property_type'].replace({'home': 1, 'land': 2}, inplace=True)

dataset['property_type'].fillna(0, inplace=True)

dataset['property_type'].unique()

"""#### Units

Rename total_units to units
"""

dataset.rename(columns={'total_units': 'units'}, inplace=True)

dataset['units'].unique()

dataset['units'].fillna('0', inplace=True)

"""Remove the 'U' suffix, convert to int64...impute NaNs to 0"""

dataset['units'] = dataset['units'].str.replace('U', '').astype(np.int64)

dataset['units'].unique()

"""#### Income"""

dataset['income'].isna().sum()

"""Impute NaNs to 0.0"""

dataset['income'].fillna(0.0, inplace=True)

dataset['income'].isna().sum()

"""#### Credit type"""

dataset['credit_type'].unique()

"""Convert EXP to 1, EQUI to 2, TRANS to 3, CRIF and CIB to 4...impute NaNs to 0"""

dataset['credit_type'].replace({'EXP': 1, 'EQUI': 2, 'TRANS': 3, 'CIB': 4, 'CRIF': 4}, inplace=True)

dataset['credit_type'].fillna(0, inplace=True)

dataset['credit_type'].unique()

"""#### Credit score"""

dataset['credit_score'].unique()

dataset['credit_score'].fillna(0, inplace=True)

dataset['credit_score'].unique()

"""#### CoBorrower credit type"""

dataset['co-applicant_credit_type'].unique()

"""Convert EXP to 1, EQUI to 2, TRANS to 3, CRIF and CIB to 4...impute NaNs to 0"""

dataset['co-applicant_credit_type'].replace({'EXP': 1, 'EQUI': 2, 'TRANS': 3, 'CIB': 4, 'CRIF': 4}, inplace=True)

dataset['co-applicant_credit_type'].fillna(0, inplace=True)

"""Rename co-applicant_credit_type to co_borrower_credit_type"""

dataset.rename(columns={'co-applicant_credit_type': 'co_borrower_credit_type'}, inplace=True)

dataset['co_borrower_credit_type'].unique()

"""#### Application taken"""

dataset['submission_of_application'].unique()

"""Convert to_inst to 1, not_inst to 2...impute NaNs to 0. Rename column application_taken"""

dataset['submission_of_application'].replace({'to_inst': 1, 'not_inst': 2}, inplace=True)

dataset['submission_of_application'].fillna(0, inplace=True)

dataset.rename(columns={'submission_of_application': 'application_taken'}, inplace=True)

dataset['application_taken'].unique()

dataset['application_taken'] = dataset['application_taken'].astype(np.int64)

dataset['application_taken'].unique()

"""#### LTV"""

dataset['ltv'].unique()

"""LTV cannot be NaN...explore the mean, median and mode of LTV for each status."""

print(dataset[dataset['status'] == 0][['ltv']].describe())
print(dataset[dataset['status'] == 1][['ltv']].describe())
print(dataset[dataset['status'] == 0][['ltv']].mode())
print(dataset[dataset['status'] == 1][['ltv']].mode())

"""The median between the two subsets is the closest of the three...impute NaN values to the median of each."""

status0_median = dataset[(dataset['status'] == 0) & (~dataset['ltv'].isna())]['ltv'].median()

dataset.loc[(dataset['status'] == 0) & (dataset['ltv'].isna()), 'ltv'] = status0_median

dataset[dataset['status'] == 0]['ltv'].unique()

status1_median = dataset[(dataset['status'] == 1) & (~dataset['ltv'].isna())]['ltv'].median()

dataset.loc[(dataset['status'] == 1) & (dataset['ltv'].isna()), 'ltv'] = status1_median

dataset[dataset['status'] == 1]['ltv'].unique()

dataset[dataset['status'] == 0]['ltv'].isna().sum()

dataset[dataset['status'] == 1]['ltv'].isna().sum()

"""#### Deposit type"""

dataset['security_type'].unique()

"""Convert direct to 1, indirect to 2...impute NaNs to 0"""

dataset['security_type'].fillna(0, inplace=True)

dataset['security_type'].replace({'direct': 1, 'Indriect': 2}, inplace=True)

dataset['security_type'] = dataset['security_type'].astype(np.int64)

dataset['security_type'].unique()

"""Rename security type to deposit type"""

dataset.rename(columns={'security_type': 'deposit_type'}, inplace=True)

dataset['deposit_type'].unique()

"""#### DTI"""

dataset['dtir1'].unique()

"""DTI cannot be NaN...explore the mean, median and mode of DTI for each status."""

print(dataset[dataset['status'] == 0][['dtir1']].describe())
print(dataset[dataset['status'] == 1][['dtir1']].describe())
print(dataset[dataset['status'] == 0][['dtir1']].mode())
print(dataset[dataset['status'] == 1][['dtir1']].mode())

"""The mean has the smallest deviation between the two sets...impute NaNs to the mean for each status set"""

status0_mean = dataset[(dataset['status'] == 0) & (~dataset['dtir1'].isna())]['dtir1'].mean()

dataset.loc[(dataset['status'] == 0) & (dataset['dtir1'].isna()), 'dtir1'] = status0_mean

dataset[dataset['status'] == 0]['dtir1'].unique()

status1_mean = dataset[(dataset['status'] == 1) & (~dataset['dtir1'].isna())]['dtir1'].mean()

dataset.loc[(dataset['status'] == 1) & (dataset['dtir1'].isna()), 'dtir1'] = status0_mean

dataset[dataset['status'] == 1]['dtir1'].unique()

print(dataset[dataset['status'] == 0]['dtir1'].isna().sum())
print(dataset[dataset['status'] == 1]['dtir1'].isna().sum())

"""Rename dtir1 to dti"""

dataset.rename(columns={'dtir1': 'dti'}, inplace=True)

dataset['dti']

"""#### Status"""

dataset['status'].unique()

"""This is the column the test split will predict. If any rows were missing a value here they would need to be dropped, however every row has either a 0 or a 1."""

dataset.columns

"""#### Fair credit

Credit cannot be determined on the basis of sex, or age. Remove these columns to avoid violating fair credit reporting laws.
"""

dataset.columns

dataset.drop(['gender', 'age'], axis=1, inplace=True)

dataset.columns

"""The region column should only be used for reporting and stress testing a portfolio to reduce disparate impact / treatment. Remove that column to avoid bias in underwriting decisions."""

dataset.drop(['region'], axis=1, inplace=True)

"""#### Build Model"""

y = dataset["status"].copy()
X = dataset.drop(["status", ], axis=1, inplace=False).copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)

X_train.reset_index(inplace=True, drop=True)
X_test.reset_index(inplace=True, drop=True)
y_train.reset_index(inplace = True, drop=True)
y_test.reset_index(inplace = True, drop=True)

# batch size
max_iter = 10000

classifier = MLPClassifier(
    hidden_layer_sizes = (20, 20), # number of neurons in the perceptron
    early_stopping = True, # after n_iter_no_change epochs stop fitting
    n_iter_no_change = 50, # number of epochs to stop after
    max_iter = max_iter # total number of epochs
)

print (classifier.fit(X_train.to_numpy(), y_train.to_numpy()))

print (f"iterations ran: {classifier.n_iter_}")
print (f"Train score: {classifier.score(X_train.to_numpy(), y_train.to_numpy())}")
print (f"Test score: {classifier.score(X_test.to_numpy(), y_test.to_numpy())}")

"""#### Evaluate Model"""

parameters = {
    'hidden_layer_sizes': [(20, 20), (25, 25)],
    'learning_rate_init': [.001, .003, .004],
    'tol': [1e-05, 5e-05, 1e-04],
}

cv = GridSearchCV(classifier, param_grid=parameters, cv=3, verbose=5, n_jobs=-1, return_train_score=True)
cv.fit(X_train.to_numpy(), y_train.to_numpy())

print ('recommended estimator:', cv.best_estimator_)
print ('recommended parameters:', cv.best_params_)
print ('best score:', cv.best_score_)

classifier_improved = cv.best_estimator_

print (f"Train score: {classifier_improved.score(X_train.to_numpy(), y_train.to_numpy())}")
print (f"Test score: {classifier_improved.score(X_test.to_numpy(), y_test.to_numpy())}")