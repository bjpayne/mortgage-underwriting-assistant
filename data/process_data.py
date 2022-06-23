# import libraries
import sys
import pandas as pd


def load_data(filepath):
    """
        Load the data into a dataframe

        INPUT
        messages_filepath - string
        categories_filepath - string

        OUTPUT
        df - A dataframe
    """
    dataset = pd.read_csv(filepath)

    return dataset


def clean_data(dataset):
    dataset.columns = dataset.columns.str.lower()

    dataset.drop('id', inplace=True, axis=1)
    dataset.drop('year', inplace=True, axis=1)

    loan_limit(dataset)

    return dataset.copy()


def loan_limit(dataset):
    dataset['loan_limit'].fillna(0, inplace=True)
    dataset['loan_limit'].replace({'cf': 1, 'ncf': 2}, inplace=True)

def preapproval(dataset):
    dataset


def save_data(df):
    df.to_csv('processed_data.csv')

def main():
    if len(sys.argv) == 1:
        filepath = sys.argv[:1]

        print(f'Loading data {filepath}')
        dataset = load_data(filepath)

        print('Cleaning data...')
        dataset = clean_data(dataset)

        print('Saving data...data/processed_data.csv')
        save_data(dataset)

        print('Cleaned data saved!')
    else:
        print('Please provide the filepath to the dataset for example python data/process_data.py '
              'data.csv')


if __name__ == '__main__':
    main()
