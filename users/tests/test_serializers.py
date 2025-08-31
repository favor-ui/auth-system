from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True}
        }

    def validate_email(self, value):
        """Validate and normalize email"""
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError(_("Enter a valid email address."))
        
        # Check if email already exists
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(_("A user with this email already exists."))
        
        return value.lower()

    def validate(self, data):
        """Validate that passwords match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'non_field_errors': [_("Passwords do not match.")]
            })
        return data

    def create(self, validated_data):
        """Create a new user"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email', '').lower()
        password = data.get('password', '')

        if not email or not password:
            raise serializers.ValidationError(_("Email and password are required."))

        # Authenticate user
        user = authenticate(username=email, password=password)
        
        if not user:
            raise AuthenticationFailed(_("Invalid credentials."))
        
        if not user.is_active:
            raise AuthenticationFailed(_("User account is disabled."))
        
        data['user'] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Validate email format"""
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError(_("Enter a valid email address."))
        return value.lower()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        """Validate that new passwords match"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                'non_field_errors': [_("New passwords do not match.")]
            })
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'is_active', 'date_joined')
        read_only_fields = ('id', 'is_active', 'date_joined')