import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd

# pip install graphviz or sudo apt-get install graphviz


def show_tree(model):
    xgb.plot_tree(model,num_trees=0)
    plt.rcParams['figure.figsize'] = [50, 10]
    plt.show()

def show_feature_importance(model):
    xgb.plot_importance(model)
    plt.rcParams['figure.figsize'] = [5, 5]
    plt.show()


def get_feature_importance(model):
    return (
        pd.Series(model.get_score(importance_type="gain"), index=model.feature_names)
        .fillna(0.0)
        .to_frame(name="importance")
        .reset_index()
        .rename(columns={"index": "feature_name"})
    )