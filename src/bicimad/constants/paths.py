PATH_STATIONS_RAW = 'data/raw/bases_bicimad.csv'
PATH_BIKES_RAW = 'data/raw/bike_data.csv'
PATH_BIKES_CLEAN = 'data/clean/bike_data_clean.csv'
PATH_AEMET_PER_DAY = 'data/raw/other-data/aemet_per_day.json'
PATH_DATASET = {
    'daily': 'data/prepared/bicimad_daily.csv',
    'hourly': 'data/prepared/bicimad_hourly.csv'
}
PATH_RESULTS = {
    'daily': {
        'random-forest':{
            'model' :'data/results/daily/randomforest/model',
            'metrics': 'data/results/daily/randomforest/metrics'
        },
        'deep-learning': {
            'model' :'data/results/daily/deeplearning/model',
            'metrics': 'data/results/daily/deeplearning/metrics'
        },
        'xgboost': {
            'model' :'data/results/daily/xgboost/model',
            'metrics': 'data/results/daily/xgboost/metrics'
        },
    },
    'hourly':
    {
        'random-forest':{
            'model' : 'data/results/hourly/randomforest/model',
            'metrics': 'data/results/hourly/randomforest/metrics'
        },
        'deep-learning': {
            'model' :'data/results/hourly/deeplearning/model',
            'metrics': 'data/results/hourly/deeplearning/metrics'
        }
    }
}