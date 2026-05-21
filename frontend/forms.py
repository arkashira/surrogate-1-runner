from django import forms
from .models import ForecastingParameters

# Create a form for users to adjust forecasting parameters
class ForecastingParametersForm(forms.ModelForm):
    class Meta:
        model = ForecastingParameters
        fields = ['look_back_period', 'forecast_horizon', 'model_type', 'seasonality']