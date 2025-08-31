import pytest

@pytest.mark.django_db
def test_create_user():
    """Test creating a regular user"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.create_user(
        email='test@example.com',
        password='TestPass!123',
        full_name='Test User'
    )
    assert user.email == 'test@example.com'
    assert user.full_name == 'Test User'
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.check_password('TestPass!123')

@pytest.mark.django_db
def test_create_superuser():
    """Test creating a superuser"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    superuser = User.objects.create_superuser(
        email='admin@example.com',
        password='AdminPass!123',
        full_name='Admin User'
    )
    assert superuser.email == 'admin@example.com'
    assert superuser.is_staff is True
    assert superuser.is_superuser is True

@pytest.mark.django_db
def test_user_str_representation():
    """Test user string representation"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = User.objects.create_user(
        email='test@example.com',
        password='TestPass!123',
        full_name='Test User'
    )
    assert str(user) == 'test@example.com'

@pytest.mark.django_db
def test_unique_email_constraint():
    """Test that email addresses must be unique"""
    from django.contrib.auth import get_user_model
    from django.db import IntegrityError
    User = get_user_model()
    
    User.objects.create_user(
        email='duplicate@example.com',
        password='TestPass!123',
        full_name='Test User'
    )
    
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email='duplicate@example.com',
            password='AnotherPass!123',
            full_name='Another User'
        )