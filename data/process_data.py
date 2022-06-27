# import libraries
import os
import pandas as pd
import numpy as np


def load_data():
    """
    Load the data into a dataframe

    OUTPUT
    dataset - Pandas.DataFrame
    """
    script_root = os.path.dirname(os.path.abspath(__file__))

    dataset = pd.read_csv(f'{script_root}/data.csv')

    return dataset


def clean_data(dataset):
    """
    Clean the data and write to /data/processed_data.csv

    INPUT
    dataset - Pandas.DataFrame
    """

    dataset.columns = dataset.columns.str.lower()

    dataset.drop('id', inplace=True, axis=1)
    dataset.drop('year', inplace=True, axis=1)

    loan_limit(dataset)
    preapproval(dataset)
    loan_type(dataset)
    loan_purpose(dataset)
    credit_worthiness(dataset)
    line_of_credit(dataset)
    commercial_loan(dataset)
    interest_rate(dataset)
    interest_rate_spread(dataset)
    upfront_charges(dataset)
    term(dataset)
    negative_amortization(dataset)
    interest_only(dataset)
    lump_sum_payment(dataset)
    property_value(dataset)
    construction_type(dataset)
    occupancy_type(dataset)
    property_type(dataset)
    units(dataset)
    income(dataset)
    credit_type(dataset)
    credit_score(dataset)
    co_borrower_credit_type(dataset)
    application_taken(dataset)
    ltv(dataset)
    deposit_type(dataset)
    dti(dataset)
    fair_credit(dataset)

    return dataset.copy()


def loan_limit(dataset):
    """
    Clean the loan_limit vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['loan_limit'].fillna(0, inplace=True)
    dataset['loan_limit'].replace({'cf': 1, 'ncf': 2}, inplace=True)


def preapproval(dataset):
    """
    Clean the pre_approval vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset.rename(columns={"approv_in_adv": "pre_approval"}, inplace=True)
    dataset['pre_approval'].fillna(0, inplace=True)
    dataset['pre_approval'].replace({'nopre': 0, 'pre': 1}, inplace=True)


def loan_type(dataset):
    """
    Clean the loan_type vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['loan_type'].fillna('0', inplace=True)
    dataset['loan_type'] = dataset['loan_type'].str.replace('type', '').astype(np.int64)


def loan_purpose(dataset):
    """
    Clean the loan_purpose vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['loan_purpose'].fillna('p0', inplace=True)
    dataset['loan_purpose'] = dataset['loan_purpose'].str.replace('p', '').astype(np.int64)


def credit_worthiness(dataset):
    """
    Clean the credit_worthiness vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset.drop(columns=['credit_worthiness'], inplace=True)


def line_of_credit(dataset):
    """
    Clean the line_of_credit vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset.rename(columns={'open_credit': 'line_of_credit'}, inplace=True)
    dataset['line_of_credit'].fillna('0', inplace=True)
    dataset['line_of_credit'].replace({'nopc': 0, 'opc': 1}, inplace=True)


def commercial_loan(dataset):
    """
    Clean the commercial_loan vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset.rename(columns={'business_or_commercial': 'commercial_loan'}, inplace=True)
    dataset['commercial_loan'].fillna(0, inplace=True)
    dataset['commercial_loan'].replace({'nob/c': 0, 'b/c': 1}, inplace=True)


def interest_rate(dataset):
    """
    Clean the interest_rate vector

    INPUT
    dataset - Pandas.DataFrame
    """
    status0_median = dataset[(dataset['status'] == 0) & (~dataset['rate_of_interest'].isna())]['rate_of_interest'].median()
    status1_median = dataset[(dataset['status'] == 1) & (~dataset['rate_of_interest'].isna())]['rate_of_interest'].median()

    dataset.loc[(dataset['status'] == 0) & (dataset['rate_of_interest'].isna()), 'rate_of_interest'] = status0_median
    dataset.loc[(dataset['status'] == 1) & (dataset['rate_of_interest'].isna()), 'rate_of_interest'] = status1_median

    dataset.rename(columns={'rate_of_interest': 'interest_rate'}, inplace=True)


def interest_rate_spread(dataset):
    """
    Clean the interest_rate_spread vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['interest_rate_spread'].fillna(0.0, inplace=True)


def upfront_charges(dataset):
    """
    Clean the interest_rate_spread vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['upfront_charges'].fillna(0.0, inplace=True)


def term(dataset):
    """
    Clean the term vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['term'] = dataset['term'].fillna(360).astype(np.int64)


def negative_amortization(dataset):
    """
    Clean the negative_amortization vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['neg_ammortization'].fillna(0, inplace=True)
    dataset['neg_ammortization'].replace({'not_neg': 0, 'neg_amm': 1}, inplace=True)
    dataset.rename(columns={'neg_ammortization': 'negative_amortization'}, inplace=True)


def interest_only(dataset):
    """
    Clean the interest_only vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['interest_only'].fillna(0)
    dataset['interest_only'].replace({'not_int': 0, 'int_only': 1}, inplace=True)


def lump_sum_payment(dataset):
    """
    Clean the lump_sum_payment vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['lump_sum_payment'].fillna(0)
    dataset['lump_sum_payment'].replace({'not_lpsm': 0, 'lpsm': 1}, inplace=True)


def property_value(dataset):
    """
    Clean the property_value vector

    INPUT
    dataset - Pandas.DataFrame
    """
    status0_median = dataset[(dataset['status'] == 0) & (~dataset['property_value'].isna())]['property_value'].median()
    status1_median = dataset[(dataset['status'] == 1) & (~dataset['property_value'].isna())]['property_value'].median()

    dataset.loc[(dataset['status'] == 0) & (dataset['property_value'].isna()), 'property_value'] = status0_median
    dataset.loc[(dataset['status'] == 1) & (dataset['property_value'].isna()), 'property_value'] = status1_median


def construction_type(dataset):
    """
    Clean the property_value vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['construction_type'].fillna(0, inplace=True)
    dataset['construction_type'].replace({'sb': 1, 'mh': 2}, inplace=True)


def occupancy_type(dataset):
    """
    Clean the occupancy_type vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['occupancy_type'].fillna(0, inplace=True)
    dataset['occupancy_type'].replace({'pr': 1, 'sr': 2, 'ir': 3}, inplace=True)


def property_type(dataset):
    """
    Clean the property_type vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset.rename(columns={'secured_by': 'property_type'}, inplace=True)
    dataset['property_type'].replace({'home': 1, 'land': 2}, inplace=True)
    dataset['property_type'].fillna(0, inplace=True)


def units(dataset):
    """
    Clean the units vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset.rename(columns={'total_units': 'units'}, inplace=True)
    dataset['units'].fillna('0', inplace=True)
    dataset['units'] = dataset['units'].str.replace('U', '').astype(np.int64)


def income(dataset):
    """
    Clean the income vector

    INPUT
    dataset - Pandas.DataFrame
    """
    status0_median = dataset[(dataset['status'] == 0) & (~dataset['income'].isna())]['income'].median()
    status1_median = dataset[(dataset['status'] == 1) & (~dataset['income'].isna())]['income'].median()

    dataset.loc[(dataset['status'] == 0) & (dataset['income'].isna()), 'income'] = status0_median
    dataset.loc[(dataset['status'] == 1) & (dataset['income'].isna()), 'income'] = status1_median


def credit_type(dataset):
    """
    Clean the credit_type vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['credit_type'].replace({'EXP': 1, 'EQUI': 2, 'TRANS': 3, 'CIB': 4, 'CRIF': 4}, inplace=True)
    dataset['credit_type'].fillna(0, inplace=True)


def credit_score(dataset):
    """
    Clean the credit_score vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['credit_score'].fillna(0, inplace=True)


def co_borrower_credit_type(dataset):
    """
    Clean the co_borrower_credit_type vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['co-applicant_credit_type'].replace({'EXP': 1, 'EQUI': 2, 'TRANS': 3, 'CIB': 4, 'CRIF': 4}, inplace=True)
    dataset['co-applicant_credit_type'].fillna(0, inplace=True)
    dataset.rename(columns={'co-applicant_credit_type': 'co_borrower_credit_type'}, inplace=True)


def application_taken(dataset):
    """
    Clean the application_taken vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['submission_of_application'].replace({'to_inst': 1, 'not_inst': 2}, inplace=True)
    dataset['submission_of_application'].fillna(0, inplace=True)
    dataset.rename(columns={'submission_of_application': 'application_taken'}, inplace=True)
    dataset['application_taken'] = dataset['application_taken'].astype(np.int64)


def ltv(dataset):
    """
    Clean the ltv vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset.loc[dataset['ltv'].isna(), 'ltv'] = ((dataset['loan_amount'] / dataset['property_value']) * 100)


def deposit_type(dataset):
    """
    Clean the deposit_type vector

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset['security_type'].fillna(0, inplace=True)
    dataset['security_type'].replace({'direct': 1, 'Indriect': 2}, inplace=True)
    dataset['security_type'] = dataset['security_type'].astype(np.int64)


def dti(dataset):
    """
    Clean the dti vector

    INPUT
    dataset - Pandas.DataFrame
    """
    status0_median = dataset[(dataset['status'] == 0) & (~dataset['dtir1'].isna())]['dtir1'].median()
    status1_median = dataset[(dataset['status'] == 1) & (~dataset['dtir1'].isna())]['dtir1'].median()

    dataset.loc[(dataset['status'] == 0) & (dataset['dtir1'].isna()), 'dtir1'] = status0_median
    dataset.loc[(dataset['status'] == 1) & (dataset['dtir1'].isna()), 'dtir1'] = status1_median

    dataset.rename(columns={'dtir1': 'dti'}, inplace=True)


def fair_credit(dataset):
    """
    Clean columns that would violate fair credit regulations

    INPUT
    dataset - Pandas.DataFrame
    """
    dataset.drop(['gender', 'age'], axis=1, inplace=True)
    dataset.drop(['region'], axis=1, inplace=True)


def save_data(dataset):
    """
    Save the dataset

    INPUT
    dataset - Pandas.DataFrame
    """
    script_root = os.path.dirname(os.path.abspath(__file__))

    file_path = f'{script_root}/processed_data.csv'

    if os.path.exists(file_path):
        os.remove(file_path)

    dataset.to_csv(file_path, index=False, mode='w+')


def main():
    print('Loading data...')
    dataset = load_data()

    print('Cleaning data...')
    dataset = clean_data(dataset)

    print('Saving data...')
    save_data(dataset)

    print('Data processed!')


if __name__ == '__main__':
    main()
