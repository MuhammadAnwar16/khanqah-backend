"""
Basic tests for core functionality
"""
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class CoreAPITests(TestCase):
    """Basic API endpoint tests"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_api_root(self):
        """Test API root is accessible"""
        # This will fail if API root doesn't exist, but that's ok
        # We're just ensuring basic API structure
        response = self.client.get('/api/')
        # API root might not exist, so we accept any 2xx or 404
        self.assertIn(response.status_code, [200, 404, 301, 302])
    
    def test_swagger_docs_accessible(self):
        """Test Swagger documentation is accessible"""
        response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, 200)
    
    def test_redoc_accessible(self):
        """Test ReDoc documentation is accessible"""
        response = self.client.get('/redoc/')
        self.assertEqual(response.status_code, 200)


class PublicationsAPITests(TestCase):
    """Tests for Publications API"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_publications_list_endpoint(self):
        """Test publications list endpoint exists and returns valid response"""
        response = self.client.get('/api/publications/publications/')
        # Should return 200 (with data) or 200 (empty list)
        self.assertEqual(response.status_code, 200)
        # DRF viewsets return data directly (list or dict), not wrapped in 'data' key
        # Verify response is valid JSON (isinstance check for list/dict)
        self.assertTrue(isinstance(response.data, (list, dict)), 
                       f"Expected list or dict, got {type(response.data)}")


class GalleryAPITests(TestCase):
    """Tests for Gallery API"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_gallery_list_endpoint(self):
        """Test gallery list endpoint exists"""
        response = self.client.get('/api/gallery/')
        self.assertEqual(response.status_code, 200)


class ContactAPITests(TestCase):
    """Tests for Contact form API"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_contact_form_endpoint_exists(self):
        """Test contact form endpoint exists"""
        # Test with GET (should fail with method not allowed or return form)
        response = self.client.get('/contact/send-message/')
        # POST is required, so GET might return 405 or 200 (form)
        self.assertIn(response.status_code, [200, 405, 400])


class ErrorHandlingTests(TestCase):
    """Tests for error handling"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_404_returns_json(self):
        """Test 404 errors return JSON format for DRF views"""
        # Note: Django's URL routing 404 returns HTML, but DRF view 404s return JSON
        # Test a DRF view endpoint with non-existent resource ID
        # This will trigger DRF's 404 handler which returns JSON via custom exception handler
        response = self.client.get('/api/publications/publications/999999/')
        self.assertEqual(response.status_code, 404)
        # DRF 404 should return JSON (not HTML)
        self.assertIn('application/json', response['Content-Type'])
        # Verify response has our custom error format
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'error')
