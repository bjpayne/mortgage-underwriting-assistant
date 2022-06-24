# import libraries
import pandas as pd
import numpy as np


def load_data():
    """
    Load the data into a dataframe

    OUTPUT
    dataset - Pandas.DataFrame
    """
    dataset = pd.read_csv('data.csv')

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
    interest_date(dataset)

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
    dataset.rename(columns={"approv_in_adv": "pre_approval"}, inplace=True)
    dataset['pre_approval'].fillna(0, inplace=True)
    dataset['pre_approval'].replace({'nopre': 0, 'pre': 1}, inplace=True)


def loan_type(dataset):
    dataset['loan_type'].fillna('0', inplace=True)
    dataset['loan_type'] = dataset['loan_type'].str.replace('type', '').astype(np.int64)


def loan_purpose(dataset):
    dataset['loan_purpose'].fillna('p0', inplace=True)
    dataset['loan_purpose'] = dataset['loan_purpose'].str.replace('p', '').astype(np.int64)


def credit_worthiness(dataset):
    dataset.drop(columns=['credit_worthiness'], inplace=True)


def line_of_credit(dataset):
    dataset.rename(columns={'open_credit': 'line_of_credit'}, inplace=True)
    dataset['line_of_credit'].fillna('0', inplace=True)
    dataset['line_of_credit'].replace({'nopc': 0, 'opc': 1}, inplace=True)


def commercial_loan(dataset):
    dataset.rename(columns={'business_or_commercial': 'commercial_loan'}, inplace=True)
    dataset['commercial_loan'].fillna(0, inplace=True)
    dataset['commercial_loan'].replace({'nob/c': 0, 'b/c': 1}, inplace=True)


def interest_date(dataset):
    status0_median = dataset[(dataset['status'] == 0) & (~dataset['rate_of_interest'].isna())]['rate_of_interest'].median()
    status1_median = dataset[(dataset['status'] == 1) & (~dataset['rate_of_interest'].isna())]['rate_of_interest'].median()

    dataset.loc[(dataset['status'] == 0) & (dataset['rate_of_interest'].isna()), 'rate_of_interest'] = status0_median
    dataset.loc[(dataset['status'] == 1) & (dataset['rate_of_interest'].isna()), 'rate_of_interest'] = status1_median

def save_data(df):
    df.to_csv('processed_data.csv')

def main():
    print(f'Loading data')
    dataset = load_data()

    print('Cleaning data...')
    dataset = clean_data(dataset)

    print('Saving data...data/processed_data.csv')
    save_data(dataset)

    print('Cleaned data saved!')


if __name__ == '__main__':
    main()
