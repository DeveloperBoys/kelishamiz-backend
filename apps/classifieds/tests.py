from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import TemporaryUploadedFile

from rest_framework import status
from rest_framework.test import APIClient


class ClassifiedCreateViewTestCase(TestCase):
    def setUp(self):
        # Create a test user and an authenticated test client
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Specify the URL for the view you want to test
        self.url = reverse('classified-create')  # Replace with your URL name

    def test_create_classified_with_valid_data(self):
        # Prepare valid data for creating a classified
        valid_data = {
            'title': 'Sample Classified',
            'category': '1',
            'detail': {
                'currencyType': 'usd',
                'price': 100.0,
                'description': "This is the classified's description.",
                'dynamicFields': [
                    {'key': 'Field 1', 'value': 'Value 1'},
                    {'key': 'Field 2', 'value': 'Value 2'}
                ]
            },
            'images': [
                {
                    'imageUrl': TemporaryUploadedFile(
                        'photo1.jpg', b'file_content', content_type='image/jpeg'
                    ),
                },
                {
                    'imageUrl': TemporaryUploadedFile(
                        'photo2.jpg', b'file_content', content_type='image/jpeg'
                    ),
                }
            ],
            'isLiked': False,
            'createdAt': '2023-09-17T11:58:13.021Z'
        }

        # Send a POST request with valid data to create a classified using JSON format
        response = self.client.post(self.url, data=valid_data, format='json')

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_classified_with_invalid_data(self):
        # Prepare invalid data (missing required fields) for creating a classified
        invalid_data = {
            'title': 'Sample Classified',
            # Missing other required fields
        }

        # Send a POST request with invalid data to create a classified
        response = self.client.post(
            self.url, data=invalid_data, format='multipart')

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Add additional assertions if needed to check the response data
        # Example: self.assertEqual(response.data['error_field'], 'Error message')
