
import pandas as pd
import plotly.express as px

def display_forecast(forecast_df):
    fig = px.line(forecast_df, x=forecast_df.index, y=['forecast', 'lower_ci', 'upper_ci'],
                  title='7-day and 30-day Forecasts')
    fig.show()

def update_and_display_forecast():
    data = get_recent_usage()
    model = ForecastModel(data)
    model.fit()
    
    forecast_7_days = model.forecast(days=7)
    forecast_30_days = model.forecast(days=30)
    
    display_forecast(forecast_7_days)
    display_forecast(forecast_30_days)

# Run the forecast display function once at startup
update_and_display_forecast()