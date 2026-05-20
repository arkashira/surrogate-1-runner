from django.contrib import admin
from .models import FounderProfile

@admin.register(FounderProfile)
class FounderProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'stage', 'target_market', 'created_at')
    search_fields = ('email', 'stage', 'target_market')
    list_filter = ('stage', 'target_market', 'pricing_model')