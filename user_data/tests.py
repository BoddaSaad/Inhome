from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cuser, Services, Order_service, OrderFile
from io import BytesIO
from PIL import Image
from unittest.mock import patch, MagicMock


class OrderFileTestCase(TestCase):
    def setUp(self):
        """Set up test client and create test data"""
        self.client = APIClient()
        
        # Create a test user
        self.user = Cuser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone='1234567890',
            latitude='30.0444',
            longitude='31.2357',
            country='Egypt',
            Provides_services=False,
            request_services=True
        )
        
        # Create a test service
        self.service = Services.objects.create(
            name='Test Service',
            name_english='Test Service',
            detal='Test Description',
            detal_by_english='Test Description'
        )
        
        # Mock the geocoding function
        self.mock_location = MagicMock()
        self.mock_location.raw = {'address': {'country': 'Egypt'}}
        self.patcher = patch('user_data.models.get_address_from_coordinates', return_value=self.mock_location)
        self.patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.patcher.stop()
    
    def create_test_image(self):
        """Create a test image file"""
        file = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'png')
        file.seek(0)
        return SimpleUploadedFile('test.png', file.read(), content_type='image/png')
    
    def test_order_file_model(self):
        """Test OrderFile model creation"""
        order = Order_service.objects.create(
            service=self.service,
            user=self.user,
            type_service='Test Type',
            time='10:00',
            latitude='30.0444',
            longitude='31.2357',
            descrtion='Test description',
            count=1
        )
        
        # Create an OrderFile
        test_file = self.create_test_image()
        order_file = OrderFile.objects.create(
            order=order,
            file=test_file
        )
        
        self.assertEqual(order_file.order, order)
        self.assertTrue(order_file.file.name.startswith('media/'))
        self.assertIsNotNone(order_file.uploaded_at)
    
    def test_order_with_multiple_files(self):
        """Test creating an order with multiple files"""
        order = Order_service.objects.create(
            service=self.service,
            user=self.user,
            type_service='Test Type',
            time='10:00',
            latitude='30.0444',
            longitude='31.2357',
            descrtion='Test description',
            count=1
        )
        
        # Add multiple files to the order
        file1 = self.create_test_image()
        file2 = self.create_test_image()
        
        OrderFile.objects.create(order=order, file=file1)
        OrderFile.objects.create(order=order, file=file2)
        
        # Check that the order has 2 files
        self.assertEqual(order.files.count(), 2)
    
    def test_order_serializer_with_files(self):
        """Test Order_serviceserlizer returns files correctly"""
        from .serializers import Order_serviceserlizer
        
        order = Order_service.objects.create(
            service=self.service,
            user=self.user,
            type_service='Test Type',
            time='10:00',
            latitude='30.0444',
            longitude='31.2357',
            descrtion='Test description',
            count=1
        )
        
        # Add files
        file1 = self.create_test_image()
        file2 = self.create_test_image()
        OrderFile.objects.create(order=order, file=file1)
        OrderFile.objects.create(order=order, file=file2)
        
        # Serialize the order
        serializer = Order_serviceserlizer(order)
        data = serializer.data
        
        # Check that files are included in the serialized data
        self.assertIn('files', data)
        self.assertEqual(len(data['files']), 2)
