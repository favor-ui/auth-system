import pytest

@pytest.mark.django_db
def test_register_serializer_valid():
    """Test valid registration data"""
    from users.serializers import RegisterSerializer
    
    data = {
        'email': 'test@example.com',
        'full_name': 'Test User',
        'password': 'StrongPass!123',
        'password_confirm': 'StrongPass!123'
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is True

@pytest.mark.django_db
def test_register_serializer_password_mismatch():
    """Test registration with mismatched passwords"""
    from users.serializers import RegisterSerializer
    
    data = {
        'email': 'test@example.com',
        'full_name': 'Test User',
        'password': 'StrongPass!123',
        'password_confirm': 'DifferentPass!123'
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is False
    assert 'non_field_errors' in serializer.errors

@pytest.mark.django_db
def test_register_serializer_weak_password():
    """Test registration with weak password"""
    from users.serializers import RegisterSerializer
    
    data = {
        'email': 'test@example.com',
        'full_name': 'Test User',
        'password': 'weak',
        'password_confirm': 'weak'
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid() is False
    assert 'password' in serializer.errors

def test_login_serializer_valid():
    """Test valid login data"""
    from users.serializers import LoginSerializer
    
    data = {
        'email': 'test@example.com',
        'password': 'StrongPass!123'
    }
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid() is True

def test_login_serializer_missing_fields():
    """Test login with missing fields"""
    from users.serializers import LoginSerializer
    
    # Missing password
    data = {'email': 'test@example.com'}
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid() is False
    
    # Missing email
    data = {'password': 'StrongPass!123'}
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid() is False