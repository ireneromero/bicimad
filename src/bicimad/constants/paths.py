PATH_STATIONS_RAW = 'data/raw/bases_bicimad.csv'
PATH_BIKES_RAW = 'data/raw/bike_data.csv'
PATH_BIKES_CLEAN = 'data/clean/bike_data_clean.csv'
PATH_AEMET_PER_DAY = 'data/raw/other-data/aemet_per_day.json'
PATH_DATASET = {
    'daily': 'data/prepared/bicimad_daily.csv',
    'hourly': 'data/prepared/bicimad_hourly.csv'
}
PATH_MODEL_DEEPLEARNING_MODEL = 'data/results/deeplearning/net'
PATH_MODEL_DEEPLEARNING_METRICS = 'data/results/deeplearning/metrics'

PATH_MODEL_RF_MODEL = 'data/results/randomforest/randomforestmodel'
PATH_MODEL_RF_METRICS = 'data/results/randomforest/metrics'

PATH_RESULTS = {
    'daily': {
        'random-forest':{
            'model' :'data/results/randomforest/daily/randomforestmodel',
            'metrics': 'data/results/randomforest/daily/metrics'
        },
        'deep-learning': {
            'model' :'data/results/deeplearning/daily/randomforestmodel',
            'metrics': 'data/results/deeplearning/daily/metrics'
        },
    },
    'hourly':
    {
        'random-forest':{
            'model' : 'data/results/randomforest/hourly/randomforestmodel',
            'metrics': 'data/results/randomforest/hourly/metrics'
        },
        'deep-learning': {
            'model' :'data/results/deeplearning/hourly/randomforestmodel',
            'metrics': 'data/results/deeplearning/hourly/metrics'
        }
    }
}