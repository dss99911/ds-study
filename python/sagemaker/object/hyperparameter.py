hyperparameters = {
    "max_depth": "5",
    "eta": "0.2",
    "alpha": "30",  # L1 regularization term on weights. Increasing this value makes models more conservative.
    "gamma": "4",  # Minimum loss reduction required to make a further partition on a leaf node of the tree. The larger, the more conservative the algorithm is.
    "lambda": "30",  # L2 regularization term on weights. Increasing this value makes models more conservative.
    "min_child_weight": "6",
    "subsample": "0.7",
    "verbosity": "1",
    "objective": "reg:linear",  # https://github.com/dmlc/xgboost/blob/master/doc/parameter.rst#learning-task-parameters
    "num_round": "50",

    # Evaluation metrics for validation data, a default metric will be assigned according to objective (rmse for regression, and logloss for classification, mean average precision for ranking)
    "eval_metric": ["auc", "logloss"] # https://github.com/dmlc/xgboost/blob/master/doc/parameter.rst#learning-task-parameters
}
