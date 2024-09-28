from datetime import timedelta
from django.utils import timezone
from .models import Brovides_services

def my_cron_job():
    ten_minutes_ago = timezone.now() - timedelta(minutes=10)
    
    # البحث عن الحسابات التي لم تصبح مديونيتها صفر منذ أكثر من 10 دقائق
    overdue_providers = Brovides_services.objects.filter(
        indebtedness__gt=0, 
        user__is_active=True, 
        debt_cleared_at__lt=ten_minutes_ago
    )
    
    for provider in overdue_providers:
        provider.user.is_active = False  # إيقاف الحساب
        provider.user.save()
        print(f"Deactivated provider: {provider.user.username}")
