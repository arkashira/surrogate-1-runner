from django.contrib.auth.models import User

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('product_type', 'target_market', 'current_traffic', 'growth_goals')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_type'].required = False
        self.fields['target_market'].required = False
        self.fields['current_traffic'].required = False
        self.fields['growth_goals'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user