import torch

params = {
    "alpha": 29,
    "colsample_bytree": 0.75,
    "gamma": 3.19,
    "lambda": 29.24,
    "max_depth": 6,
    "min_child_weight": 29.75,
    "subsample": 0.69,
    "max_cat_to_onehot": 32,
    "early_stopping_rounds": 100,
}

if torch.cuda.is_available():
    print("Training using GPU")
    params.update({"tree_method": "gpu_hist", "predictor": "cpu_predictor"})
else:
    params.update({"tree_method": "hist"})


clf_params = {"objective": "binary:logistic", "eval_metric": ["auc", "logloss"]}
params.update(clf_params)
