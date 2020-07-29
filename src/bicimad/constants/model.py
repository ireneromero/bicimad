from bicimad.constants.rides import COL_BIKES_DAY_OF_WEEK, COL_BIKES_WEEKEND, COL_BIKES_RIDES_MEAN_WEEKDAY, \
    COL_BIKES_RIDES
from bicimad.constants.weather import COL_WEATHER_TEMP_MEAN, COL_WEATHER_TEMP_MIN, COL_WEATHER_TEMP_MAX, \
    COL_WEATHER_RAIN, COL_WEATHER_WIND_MEAN

# ------------------------------------------------ Daily model ---------------------------------------------------
# ---------------------------------------------- Generic constants -----------------------------------------------
TEST_SIZE = 0.2

COLUMNS_TO_TRANSFORM_TYPE_DAILY = [COL_WEATHER_TEMP_MEAN, COL_WEATHER_TEMP_MIN, COL_WEATHER_TEMP_MAX]

CATEGORICAL_COLUMNS_DAILY = [
    COL_BIKES_DAY_OF_WEEK,
    COL_BIKES_WEEKEND
]
# TODO create new set of constants for dataset (using COL_BIKES_* and COL_WEATHER_*)?
NUMERICAL_COLUMNS_DAILY = [
    COL_BIKES_RIDES_MEAN_WEEKDAY,
    COL_WEATHER_TEMP_MEAN,
    COL_WEATHER_TEMP_MIN,
    COL_WEATHER_TEMP_MAX,
    COL_WEATHER_RAIN,
    COL_WEATHER_WIND_MEAN
]

ENCODED_CATEGORICAL_COLUMNS_DAILY = ['weekend_weekday', 'weekend_weekend']

# 'day_of_week_Fri', 'day_of_week_Mon', 'day_of_week_Sat',
#        'day_of_week_Sun', 'day_of_week_Thu', 'day_of_week_Tue',
#        'day_of_week_Wed',

FEATURES_DAILY = ENCODED_CATEGORICAL_COLUMNS_DAILY + NUMERICAL_COLUMNS_DAILY
TARGET = COL_BIKES_RIDES
# -------------------------------------------------- RF Model ----------------------------------------------------

GRID_SEARCH_PARAMETERS_RF = [
    {
        'n_estimators': [10, 20],
        'max_depth': [70, 80],
        'min_samples_leaf': [2, 3],
    }
]
# -------------------------------------------------- XGB Model ----------------------------------------------------
GRID_SEARCH_PARAMETERS_XGB = {
    'n_estimators': [100, 200, 500, 1000, 5000],
    'max_depth':[3, 5, 7, 9, 10, 15],
    'objective':['reg:squarederror']
}

# -------------------------------------------- Deep Learning Model ------------------------------------------------
# deep learning model
HIDDEN_DIMENSION = 32
EPOCHS = 100


# ------------------------------------------------ Hourly model ---------------------------------------------------
# ---------------------------------------------- Generic constants ------------------------------------------------



