import numpy as np
from sklearn.ensemble import RandomForestRegressor

from bicimad.constants.model import GRID_SEARCH_PARAMETERS_RF, TARGET, MODEL_FEATURES
from bicimad.modeling.utils import grid_search_cv, evaluate, predict, prepare_data


def random_forest_model(dataset, sampling_frequency='daily', feature_importance=True):
    FEATURES = MODEL_FEATURES[sampling_frequency]  # depending on sampling_frequency
    dataset_train, dataset_test = prepare_data(dataset, sampling_frequency)
    rf_model = RandomForestRegressor()
    rf_model_best = grid_search_cv(rf_model,
                                   parameters_grid=GRID_SEARCH_PARAMETERS_RF,
                                   train_features=dataset_train[FEATURES],
                                   train_target=dataset_train[TARGET]).best_estimator_
    rf_model_best.fit(dataset_train[FEATURES], dataset_train[TARGET])
    predictions = predict(rf_model_best, dataset_test[FEATURES])
    metrics = evaluate(predictions,
                       test_target=dataset_test[TARGET])
    if feature_importance:
        feature_importances_result = {}
        feature_importances = rf_model_best.feature_importances_
        sorted_features_idx = np.argsort(feature_importances)
        sorted_features_importances = feature_importances[sorted_features_idx]
        ordered_features = dataset_train[FEATURES].columns[sorted_features_idx]
        for feature, importance in zip(ordered_features, sorted_features_importances):
            feature_importances_result[feature] = importance
        return rf_model_best, metrics, feature_importances_result
    return rf_model_best, metrics


def random_forest_feature_importance(regressor: RandomForestRegressor):
    return regressor.feature_importances_



