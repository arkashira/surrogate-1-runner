from django.shortcuts import render
from .forms import ForecastingParametersForm

# Create a view for users to adjust forecasting parameters
def forecasting_parameters_view(request):
    if request.method == 'POST':
        form = ForecastingParametersForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ForecastingParametersForm()
    return render(request, 'frontend/forecasting_parameters.html', {'form': form})