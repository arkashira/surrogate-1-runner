from forecasting import ForecastModel

def main():
    historical_data = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145]
    model = ForecastModel(historical_data)
    model.train()
    forecast = model.predict(30)
    model.plot_forecast(forecast)

if __name__ == '__main__':
    main()