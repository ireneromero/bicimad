from xgboost import XGBRegressor
from bicimad.constants.model import FEATURES_DAILY, TARGET, GRID_SEARCH_PARAMETERS_XGB
from bicimad.modeling.utils import prepare_data, grid_search_cv, evaluate


def xgboost_model(dataset):
    dataset_train, dataset_test = prepare_data(dataset)
    #data_train = xgb.DMatrix(dataset_train[FEATURES_DAILY], label=dataset_train[TARGET])

    xgb_model = XGBRegressor()
    xgb_model_best = grid_search_cv(xgb_model,
                                   parameters_grid=GRID_SEARCH_PARAMETERS_XGB,
                                   train_features=dataset_train[FEATURES_DAILY],
                                   train_target=dataset_train[TARGET]).best_estimator_
    xgb_model_best.fit(dataset_train[FEATURES_DAILY], dataset_train[TARGET])
    metrics = evaluate(xgb_model_best,
                       test_features=dataset_test[FEATURES_DAILY],
                       test_target=dataset_test[TARGET])
    return xgb_model, metrics

