import xgboost as xgb
from sklearn.datasets import make_classification
from xgboosts import xgboost_params
X = make_classification()

train_data = xgb.DMatrix(
    X.loc, missing=0.0, label=y, enable_categorical=True
)

bst = xgb.train(
    xgboost_params.params,
    train_data,
    num_boost_round=100000,
    evals=evals,
    verbose_eval=100,
    xgb_model=xgb_model,
    callbacks=callbacks,
)


