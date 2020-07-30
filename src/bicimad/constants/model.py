from bicimad.constants.rides import COL_BIKES_DAY_OF_WEEK, COL_BIKES_WEEKEND, COL_BIKES_RIDES_MEAN_WEEKDAY, \
    COL_BIKES_RIDES, COL_BIKES_HOUR, COL_BIKES_RIDES_MEAN_WEEKDAY_HOUR
from bicimad.constants.weather import COL_WEATHER_TEMP_MEAN, COL_WEATHER_TEMP_MIN, COL_WEATHER_TEMP_MAX, \
    COL_WEATHER_RAIN, COL_WEATHER_WIND_MEAN, COL_WEATHER_TEMP_HOURLY, COL_WEATHER_WIND_HOURLY, COL_WEATHER_RAIN_HOURLY

# ------------------------------------------------ Daily model ---------------------------------------------------
# ---------------------------------------------- Generic constants -----------------------------------------------
TEST_SIZE = 0.2

DAILY = 'daily'
HOURLY = 'hourly'

COLUMNS_TO_TRANSFORM_TYPE = {
    DAILY: [COL_WEATHER_TEMP_MEAN, COL_WEATHER_TEMP_MIN, COL_WEATHER_TEMP_MAX],
    HOURLY: [COL_WEATHER_TEMP_HOURLY, COL_WEATHER_TEMP_MIN, COL_WEATHER_TEMP_MAX]
}

CATEGORICAL_COLUMNS_DAILY = [
    COL_BIKES_DAY_OF_WEEK,
    COL_BIKES_WEEKEND
]

CATEGORICAL_COLUMNS_HOURLY = [
    COL_BIKES_DAY_OF_WEEK,
    COL_BIKES_WEEKEND,
    COL_BIKES_HOUR
]

CATEGORICAL_COLUMNS = {
    DAILY: CATEGORICAL_COLUMNS_DAILY,
    HOURLY: CATEGORICAL_COLUMNS_HOURLY
}

# TODO create new set of constants for dataset (using COL_BIKES_* and COL_WEATHER_*)?
NUMERICAL_COLUMNS_DAILY = [
    COL_BIKES_RIDES_MEAN_WEEKDAY,
    COL_WEATHER_TEMP_MEAN,
    COL_WEATHER_TEMP_MIN,
    COL_WEATHER_TEMP_MAX,
    COL_WEATHER_RAIN,
    COL_WEATHER_WIND_MEAN
]

NUMERICAL_COLUMNS_HOURLY = [
    COL_BIKES_RIDES_MEAN_WEEKDAY_HOUR,
    COL_WEATHER_TEMP_MAX,
    COL_WEATHER_TEMP_MIN,
    COL_WEATHER_TEMP_HOURLY,
    COL_WEATHER_RAIN_HOURLY,
    COL_WEATHER_WIND_HOURLY
]

ENCODED_CATEGORICAL_COLUMNS_DAILY = ['weekend_weekday', 'weekend_weekend', 'day_of_week_Fri', 'day_of_week_Mon',
                                     'day_of_week_Sat', 'day_of_week_Sun', 'day_of_week_Thu', 'day_of_week_Tue',
                                     'day_of_week_Wed']

ENCODED_CATEGORICAL_COLUMNS_HOURLY = ['day_of_week_Fri', 'day_of_week_Mon', 'day_of_week_Sat',
       'day_of_week_Sun', 'day_of_week_Thu', 'day_of_week_Tue',
       'day_of_week_Wed', 'weekend_weekday', 'weekend_weekend', 'hour_0',
       'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7',
       'hour_8', 'hour_9', 'hour_10', 'hour_11', 'hour_12', 'hour_13',
       'hour_14', 'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19',
       'hour_20', 'hour_21', 'hour_22', 'hour_23']


# 'day_of_week_Fri', 'day_of_week_Mon', 'day_of_week_Sat',
#        'day_of_week_Sun', 'day_of_week_Thu', 'day_of_week_Tue',
#        'day_of_week_Wed',

FEATURES_DAILY = ENCODED_CATEGORICAL_COLUMNS_DAILY + NUMERICAL_COLUMNS_DAILY
FEATURES_HOURLY = ENCODED_CATEGORICAL_COLUMNS_HOURLY + NUMERICAL_COLUMNS_HOURLY
TARGET = COL_BIKES_RIDES

MODEL_FEATURES = {
    DAILY: FEATURES_DAILY,
    HOURLY: FEATURES_HOURLY
}
# -------------------------------------------------- RF Model ----------------------------------------------------

GRID_SEARCH_PARAMETERS_RF = [
    {
        'n_estimators': [10, 20],
        'max_depth': [5, 15, 30],
        'min_samples_leaf': [2, 5, 10],
    }
]
# -------------------------------------------------- XGB Model ----------------------------------------------------
GRID_SEARCH_PARAMETERS_XGB = {
    'n_estimators': [100, 200, 500, 1000, 5000],
    'max_depth':[3, 5, 7, 9, 10, 15],
    'objective':['reg:squarederror'],
    'lambda':[0.1, 0.4, 1]
}

# -------------------------------------------- Deep Learning Model ------------------------------------------------
# deep learning model
HIDDEN_DIMENSION = 32
EPOCHS = 100





# ---------------------------------------------- Generic constants ------------------------------------------------



