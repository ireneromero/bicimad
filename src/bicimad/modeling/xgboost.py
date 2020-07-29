from xgboost import XGBRegressor
from bicimad.constants.model import TARGET, GRID_SEARCH_PARAMETERS_XGB, MODEL_FEATURES
from bicimad.modeling.utils import prepare_data, grid_search_cv, evaluate, predict


def xgboost_model(dataset, sampling_frequency='daily'):
    FEATURES = MODEL_FEATURES[sampling_frequency] # depending on sampling_frequency
    dataset_train, dataset_test = prepare_data(dataset, sampling_frequency)
    xgb_model = XGBRegressor()
    xgb_model_best = grid_search_cv(xgb_model,
                                   parameters_grid=GRID_SEARCH_PARAMETERS_XGB,
                                   train_features=dataset_train[FEATURES],
                                   train_target=dataset_train[TARGET]).best_estimator_
    xgb_model_best.fit(dataset_train[FEATURES], dataset_train[TARGET])
    predictions = predict(xgb_model_best, dataset_test[FEATURES])
    metrics = evaluate(predictions,
                       test_target=dataset_test[TARGET])
    return xgb_model, metrics

