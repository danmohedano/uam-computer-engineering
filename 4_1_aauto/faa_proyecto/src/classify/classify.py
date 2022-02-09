from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
import numpy as np
import logging


def score_classifier(clf, X, y, n_splits):
    """Scores a classifier using KFold cross validation.

    Args:
        clf (Classifier): Classifier.
        X (np.ndarray): Data.
        y (np.ndarray): Class data.
        n_splits (int): Number of splits for KFold cross validation.

    Returns:
        float: Mean score.
        float: Stdandard deviation of scores.
    """
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=0)
    scores = []
    counter = 1

    for train_index, test_index in kf.split(X):
        logging.info(f'---Executing split #{counter}/{n_splits}...')
        # Train classifier
        clf.fit(X[train_index], y[train_index])
        scores.append(clf.score(X[test_index], y[test_index]))
        counter += 1

    return (np.mean(scores), np.std(scores))


def build_confusion_matrix(clf, X, y):
    """Builds the confusion matrix with an already trained classifier.

    Args:
        clf (Classifier): Trained classifier.
        X (np.ndarray): Data.
        y (np.ndarray): Class data.

    Returns:
        np.ndarray: Confusion matrix.
    """
    # Predict data
    predictions = clf.predict(X)

    return confusion_matrix(y, predictions)


def build_roc_space(cm):
    """Calculates the ROC space for data.
    
    Args:
        cm (np.ndarray): Confusion matrix.

    Returns:
        np.ndarray: FPR per class.
        np.ndarray: TPR per class.
    """
    fpr = np.zeros(3)
    tpr = np.zeros(3)

    for i in range(cm.shape[0]):
        tp = cm[i,i]
        fp = sum(cm[:,i]) - tp
        fn = sum(cm[i,:]) - tp
        tn = cm.sum() - tp - fp - fn

        fpr[i] = fp / (fp + tn)
        tpr[i] = tp / (tp + fn)

    return fpr, tpr


    