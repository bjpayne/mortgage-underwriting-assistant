# import libraries
import pickle

import pandas as pd

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPClassifier


def load_data():
    """
    Load the data into the script

    OUTPUT
    dataset - Pandas.DataFrame
    """
    dataset = pd.read_csv('../data/processed_data.csv')

    y = dataset["status"].copy()
    X = dataset.drop(["status", ], axis=1, inplace=False).copy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=40)

    X_train.reset_index(inplace=True, drop=True)
    X_test.reset_index(inplace=True, drop=True)
    y_train.reset_index(inplace=True, drop=True)
    y_test.reset_index(inplace=True, drop=True)

    return dataset, X_train, X_test, y_train, y_test


def build_model(X_train, X_test, y_train, y_test):
    """
    Build the MLPClassifier

    OUTPUT
    pipeline sklearn.Pipeline
    """
    # batch size
    max_iter = 10000

    classifier = MLPClassifier(
        hidden_layer_sizes=(20, 20),  # number of neurons in the perceptron
        early_stopping=True,  # after n_iter_no_change epochs stop fitting
        n_iter_no_change=50,  # number of epochs to stop after
        max_iter=max_iter  # total number of epochs
    )

    print(classifier.fit(X_train.to_numpy(), y_train.to_numpy()))

    print(f"iterations ran: {classifier.n_iter_}")
    print(f"Train score: {classifier.score(X_train.to_numpy(), y_train.to_numpy())}")
    print(f"Test score: {classifier.score(X_test.to_numpy(), y_test.to_numpy())}")

    return classifier


def improve_model(classifier, X_train, y_train, X_test, y_test):
    """
    Improve the classifier with GridSearchCV

    OUTPUT
    pipeline sklearn.Pipeline
    """
    parameters = {
        'hidden_layer_sizes': [(20, 20), (25, 25)],
        'learning_rate_init': [.001, .003, .004],
        'tol': [1e-05, 5e-05, 1e-04],
    }

    cv = GridSearchCV(classifier, param_grid=parameters, cv=3, verbose=5, n_jobs=-1, return_train_score=True)

    print(cv.fit(X_train.to_numpy(), y_train.to_numpy()))
    print(f"recommended estimator: {cv.best_estimator_}")
    print(f"recommended parameters: {cv.best_params_}")
    print(f"best score: {cv.best_score_}")

    classifier_improved = cv.best_estimator_

    print(f"Train score: {classifier_improved.score(X_train.to_numpy(), y_train.to_numpy())}")
    print(f"Test score: {classifier_improved.score(X_test.to_numpy(), y_test.to_numpy())}")

    return cv



def evaluate_model(cv, X_test, y_test):
    """
    Evaluate the model and print out a classification report

    INPUT
    model - sklearn.Pipeline
    X_test - sklearn.List
    Y_test - sklearn.List
    """
    y_pred = cv.predict(X_test.to_numpy())

    print(classification_report(y_test, y_pred))
    print()


def save_model(model):
    """
        Save the completed model for re-use

        INPUT
        model - sklearn.Pipeline
        model_filepath - string
    """
    filename = 'model.sav';

    pickle.dump(model, open(filename, 'wb'))


def main():
    print('Loading cleaned data...')
    dataset, X_train, X_test, y_train, y_test = load_data()

    print('Building the model...')
    classifier = build_model(X_train, X_test, y_train, y_test)

    print('Grid search...')
    cv = improve_model(classifier, X_train, y_train, X_test, y_test)

    print('Evaluate the model...')
    evaluate_model(cv, X_test, y_test)

    print('Save the model...')
    save_model(cv)


if __name__ == '__main__':
    main()
