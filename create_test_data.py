#!/usr/bin/env python
"""
Simple script to create a superuser and sample data for testing
"""
import os
import sys
import django

# Add the project root to the Python path
sys.path.append('.')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model
from user_data.models import Services, Brovides_services
from decimal import Decimal

User = get_user_model()

def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(email='admin@example.com').exists():
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            phone='+1234567890',
            country='Egypt',
            location='Cairo, Egypt',
            latitude='30.0444',
            longitude='31.2357',
            name='Admin User',
            is_staff=True,
            is_superuser=True
        )
        admin.set_password('admin123')
        admin.save()
        print(f'✅ Created superuser: {admin.email}')
        return admin
    else:
        print('⚠️ Superuser already exists')
        return User.objects.get(email='admin@example.com')

def create_services():
    """Create sample services"""
    services_data = [
        {
            'name': 'إصلاح السباكة',
            'name_english': 'Plumbing Repair',
            'detal': 'خدمات إصلاح وصيانة السباكة المنزلية',
            'detal_by_english': 'Home plumbing repair and maintenance services'
        },
        {
            'name': 'إصلاح الكهرباء',
            'name_english': 'Electrical Repair',
            'detal': 'خدمات إصلاح وصيانة الكهرباء المنزلية',
            'detal_by_english': 'Home electrical repair and maintenance services'
        },
        {
            'name': 'تنظيف المنزل',
            'name_english': 'House Cleaning',
            'detal': 'خدمات تنظيف المنزل الشاملة',
            'detal_by_english': 'Comprehensive house cleaning services'
        }
    ]
    
    created_services = []
    for service_data in services_data:
        service, created = Services.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            print(f'✅ Created service: {service.name}')
        created_services.append(service)
    
    return created_services

def create_test_users(services):
    """Create test users"""
    # Create a client
    if not User.objects.filter(email='client@example.com').exists():
        client = User.objects.create_user(
            username='client_user',
            email='client@example.com',
            phone='+201234567890',
            country='Egypt',
            location='Cairo, Egypt',
            latitude='30.0444',
            longitude='31.2357',
            name='Ahmed Mohamed',
            Provides_services=False,
            request_services=True,
            lan='A'
        )
        client.set_password('password123')
        client.save()
        print(f'✅ Created client: {client.email}')
    
    # Create a service provider
    if not User.objects.filter(email='provider@example.com').exists():
        provider = User.objects.create_user(
            username='provider_user',
            email='provider@example.com',
            phone='+201234567891',
            country='Egypt',
            location='Cairo, Egypt',
            latitude='30.0444',
            longitude='31.2357',
            name='Mohamed Hassan',
            Provides_services=True,
            request_services=False,
            lan='A'
        )
        provider.set_password('password123')
        provider.save()
        
        # Create Brovides_services entry
        if services:
            Brovides_services.objects.create(
                user=provider,
                service=services[0],  # Plumbing service
                rating=4.5
            )
        
        print(f'✅ Created service provider: {provider.email}')

if __name__ == '__main__':
    print('🚀 Creating sample data...')
    
    # Create superuser
    admin = create_superuser()
    
    # Create services
    services = create_services()
    
    # Create test users
    create_test_users(services)
    
    print('\n✅ Sample data created successfully!')
    print('\n📋 Test Credentials:')
    print('🔑 Superuser: admin@example.com / admin123')
    print('👤 Client: client@example.com / password123')
    print('🔧 Provider: provider@example.com / password123')
    print('\n🚀 You can now test the endpoints!')
