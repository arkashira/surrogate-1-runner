from django.shortcuts import render, redirect
from .forms import QuestionnaireForm

def questionnaire(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = QuestionnaireForm()
    return render(request, 'questionnaire.html', {'form': form})

def success(request):
    return render(request, 'success.html')