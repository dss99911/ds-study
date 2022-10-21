from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


def show_target_distribution(y, lim=None):
    f, ax = plt.subplots(1, 1)

    ax.hist(y, bins=100, density=True)
    ax.set_ylabel("Probability")
    ax.set_xlabel("Target")
    ax.set_title("Target distribution")
    if lim:
        ax.set_xlim(lim)
        ax.set_ylim(lim)
    plt.show()


def show_prediction_scatter(y_test, y_pred, lim=None):
    f, ax = plt.subplots(1, 1)
    ax.scatter(y_test, y_pred, s=1)
    ax.set_ylabel("Target predicted")
    ax.set_xlabel("True Target")
    ax.set_title("Prediction Scatter")
    if lim:
        ax.set_xlim(lim)
        ax.set_ylim(lim)
    # Transform targets and use same linear model
    plt.show()


def show_feature_importance(model, feature_names):
    """
    https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
    """
    forest_importances = pd.Series(model.feature_importances_, index=feature_names)

    fig, ax = plt.subplots()
    std = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()


def show_feature_importance_permutation(model, X_test, y_test, feature_names):
    from sklearn.inspection import permutation_importance

    result = permutation_importance(
        model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2
    )
    forest_importances = pd.Series(result.importances_mean, index=feature_names)
    fig, ax = plt.subplots()

    forest_importances.plot.bar(yerr=result.importances_std, ax=ax)
    ax.set_title("Feature importances using permutation on full model")
    ax.set_ylabel("Mean accuracy decrease")
    fig.tight_layout()
    plt.show()
