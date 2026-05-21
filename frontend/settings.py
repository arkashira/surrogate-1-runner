from django.conf import settings

# Add forecasting parameters to settings
settings.FORECASTING_PARAMETERS = {
    'look_back_period': 30,
    'forecast_horizon': 12,
    'model_type': 'ARIMA',
    'seasonality': True,
}