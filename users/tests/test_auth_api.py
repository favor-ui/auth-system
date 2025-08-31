import pytest

@pytest.mark.django_db
def test_register_and_login_flow():
    """Test user registration and login flow"""
    from rest_framework.test import APIClient
    client = APIClient()
    
    # Register
    response = client.post('/api/auth/register/', {
        'full_name': 'Test User',
        'email': 'test@example.com',
        'password': 'StrongPass!123',
        'password_confirm': 'StrongPass!123'
    }, format='json')
    assert response.status_code == 201
    assert 'email' in response.json()
    assert response.json()['email'] == 'test@example.com'

    # Login
    response = client.post('/api/auth/login/', {
        'email': 'test@example.com',
        'password': 'StrongPass!123'
    }, format='json')
    assert response.status_code == 200
    data = response.json()
    assert 'access' in data
    assert 'refresh' in data
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'

@pytest.mark.django_db
def test_password_reset_flow():
    """Test password reset flow"""
    from rest_framework.test import APIClient
    from django.contrib.auth import get_user_model
    User = get_user_model()
    client = APIClient()
    
    # Create user
    user = User.objects.create_user(
        email='test2@example.com', 
        password='Initial!234', 
        full_name='Test User'
    )
    
    # Request password reset
    response = client.post('/api/auth/forgot-password/', {
        'email': 'test2@example.com'
    }, format='json')
    assert response.status_code == 200
    data = response.json()
    
    # In debug mode, we should get a token back
    if 'token' in data:
        token = data['token']
        
        # Reset password with token
        response = client.post('/api/auth/reset-password/', {
            'token': token,
            'new_password': 'NewPass!456',
            'new_password_confirm': 'NewPass!456'
        }, format='json')
        assert response.status_code == 200
        
        # Try to login with new password
        response = client.post('/api/auth/login/', {
            'email': 'test2@example.com',
            'password': 'NewPass!456'
        }, format='json')
        assert response.status_code == 200
        assert 'access' in response.json()

@pytest.mark.django_db
def test_invalid_login():
    """Test login with invalid credentials"""
    from rest_framework.test import APIClient
    from django.contrib.auth import get_user_model
    User = get_user_model()
    client = APIClient()
    
    User.objects.create_user(
        email='test3@example.com',
        password='CorrectPass!123',
        full_name='Test User'
    )
    
    # Wrong password
    response = client.post('/api/auth/login/', {
        'email': 'test3@example.com',
        'password': 'WrongPassword!'
    }, format='json')
    assert response.status_code == 400
    
    # Non-existent user
    response = client.post('/api/auth/login/', {
        'email': 'nonexistent@example.com',
        'password': 'SomePassword!'
    }, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_user_profile():
    """Test getting user profile with authentication"""
    from rest_framework.test import APIClient
    from django.contrib.auth import get_user_model
    User = get_user_model()
    client = APIClient()
    
    # Create user and get tokens
    user = User.objects.create_user(
        email='test4@example.com',
        password='TestPass!123',
        full_name='Test User'
    )
    
    # Login to get token
    response = client.post('/api/auth/login/', {
        'email': 'test4@example.com',
        'password': 'TestPass!123'
    }, format='json')
    assert response.status_code == 200
    access_token = response.json()['access']
    
    # Get profile with authentication
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.get('/api/auth/me/')
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'test4@example.com'
    assert data['full_name'] == 'Test User'

@pytest.mark.django_db
def test_healthcheck():
    """Test healthcheck endpoint"""
    from rest_framework.test import APIClient
    client = APIClient()
    
    response = client.get('/health/')
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert 'services' in data
    assert 'timestamp' in data