from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .task_filter import TaskFilterForm
from surrogate_1.models import Task

class TaskDashboard(View):
    template_name = 'task_dashboard.html'
    edit_template_name = 'task_edit.html'
    
    def get(self, request):
        edit_task_id = request.GET.get('edit')
        if edit_task_id:
            return self.handle_edit_view(request, edit_task_id)
        return self.render_dashboard(request)
    
    def handle_edit_view(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, self.edit_template_name, {'task': task})
    
    def render_dashboard(self, request):
        filter_form = TaskFilterForm(request.GET)
        tasks = Task.objects.all()
        
        if filter_form.is_valid():
            status = filter_form.cleaned_data.get('status')
            platform = filter_form.cleaned_data.get('platform')
            
            if status:
                tasks = tasks.filter(status=status)
            if platform:
                tasks = tasks.filter(platform=platform)
                
        return render(request, self.template_name, {
            'tasks': tasks,
            'filter_form': filter_form
        })
        
    def post(self, request):
        task_id = request.POST.get('task_id')
        if not task_id:
            messages.error(request, "Task ID is required")
            return redirect('task_dashboard')
            
        task = get_object_or_404(Task, id=task_id)
        
        # Update task fields from POST data
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.status = request.POST.get('status', task.status)
        task.platform = request.POST.get('platform', task.platform)
        
        due_date = request.POST.get('due_date')
        if due_date:
            task.due_date = due_date
            
        task.save()
        messages.success(request, f"Task '{task.title}' updated successfully")
        return redirect('task_dashboard')