from django import forms

class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    
    PLATFORM_CHOICES = [
        ('', 'All Platforms'),
        ('fiverr', 'Fiverr'),
        ('upwork', 'Upwork'),
        ('freelancer', 'Freelancer.com'),
        ('toptal', 'Toptal')
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='Filter by Status',
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
            'onchange': 'this.form.submit()'
        })
    )
    
    platform = forms.ChoiceField(
        choices=PLATFORM_CHOICES,
        required=False,
        label='Filter by Platform',
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
            'onchange': 'this.form.submit()'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data