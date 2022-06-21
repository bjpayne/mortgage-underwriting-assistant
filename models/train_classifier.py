# import libraries
import pickle
import nltk
import sqlite3
import sys

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

from models.tokenizer import tokenize


def load_data(database_filepath):
    """
        Load the data into the script

        INPUT
        database_filepath - string

        OUTPUT
        X - Pandas.DataFrame
        y - Pandas.DataFrame
        category_names = Pandas.Series
    """
    conn = sqlite3.connect(database_filepath)
    df = pd.read_sql('SELECT * FROM categorized_messages', conn)

    X = df['message']
    y = df.drop(['index', 'id', 'message', 'original', 'genre'], axis=1).copy()

    y.fillna(0)

    category_names = y.columns

    return X, y, category_names


def build_model():
    """
        Builds the ML pipeline to use to train the model.

        OUTPUT
        pipeline sklearn.Pipeline
    """
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])

    parameters = {
        'vect__max_df': [0.7, 0.8, 0.9],
        'clf__estimator__n_estimators': [50, 75, 100]
    }

    cv = GridSearchCV(pipeline, param_grid=parameters, cv=3, verbose=3, n_jobs=-1)

    return cv

def evaluate_model(model, X_test, Y_test, category_names):
    """
        Evaluate the model and print out a classification report

        INPUT
        model - sklearn.Pipeline
        X_test - sklearn.List
        Y_test - sklearn.List
        category_names - Pandas.Series
    """
    Y_pred = model.predict(X_test)

    print(classification_report(Y_test, Y_pred, target_names=category_names))

def save_model(model, model_filepath):
    """
        Save the completed model for re-use

        INPUT
        model - sklearn.Pipeline
        model_filepath - string
    """
    filename = model_filepath

    pickle.dump(model, open(filename, 'wb'))

def main():
    if len(sys.argv) == 3:
        # Download nltk packages
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')

        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, y, category_names = load_data(database_filepath)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)

        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '
              'as the first argument and the filepath of the pickle file to '
              'save the model to as the second argument. \n\nExample: python '
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
