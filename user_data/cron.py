
from datetime import timedelta
from django.utils import timezone
from .models import Brovides_services

def my_cron_job():
    two_days_ago = timezone.now() - timedelta(days=1)
    overdue_providers = Brovides_services.objects.filter(indebtedness__gt=0, user__is_active=True, updated_at__lt=two_days_ago)
    
    for provider in overdue_providers:
        provider.user.is_active = False  # إيقاف الحساب
        provider.user.save()
        print(f"Deactivated provider: {provider.user.username}")
        
