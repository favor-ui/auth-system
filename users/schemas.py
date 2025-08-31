from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import status
from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    ForgotPasswordSerializer, 
    ResetPasswordSerializer, 
    UserSerializer
)

# Register schema
register_schema = extend_schema(
    tags=['Authentication'],
    request=RegisterSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="User created successfully",
            response=UserSerializer,
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={
                        'id': 1,
                        'email': 'user@example.com',
                        'full_name': 'John Doe',
                        'is_active': True,
                        'date_joined': '2023-01-01T00:00:00Z'
                    }
                )
            ]
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Validation error",
            examples=[
                OpenApiExample(
                    'Error Response',
                    value={
                        'email': ['This field is required.'],
                        'password': ['This password is too common.']
                    }
                )
            ]
        )
    },
    examples=[
        OpenApiExample(
            'Register Example',
            value={
                'email': 'user@example.com',
                'password': 'securepassword123',
                'password_confirm': 'securepassword123',
                'full_name': 'John Doe'
            }
        )
    ]
)

# Login schema
login_schema = extend_schema(
    tags=['Authentication'],
    request=LoginSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Login successful",
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={
                        'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                        'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                        'user': {
                            'id': 1,
                            'email': 'user@example.com',
                            'full_name': 'John Doe',
                            'is_active': True,
                            'date_joined': '2023-01-01T00:00:00Z'
                        }
                    }
                )
            ]
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Invalid credentials",
            examples=[
                OpenApiExample(
                    'Error Response',
                    value={'detail': 'Invalid credentials'}
                )
            ]
        )
    },
    examples=[
        OpenApiExample(
            'Login Example',
            value={
                'email': 'user@example.com',
                'password': 'securepassword123'
            }
        )
    ]
)

# Forgot password schema
forgot_password_schema = extend_schema(
    tags=['Password Management'],
    request=ForgotPasswordSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Password reset email sent",
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={'message': 'If the email exists, a reset link has been sent'}
                )
            ]
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Validation error",
            examples=[
                OpenApiExample(
                    'Error Response',
                    value={'email': ['Enter a valid email address.']}
                )
            ]
        )
    },
    examples=[
        OpenApiExample(
            'Forgot Password Example',
            value={'email': 'user@example.com'}
        )
    ]
)

# Reset password schema
reset_password_schema = extend_schema(
    tags=['Password Management'],
    request=ResetPasswordSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="Password updated successfully",
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={'message': 'Password updated successfully'}
                )
            ]
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Invalid token or validation error",
            examples=[
                OpenApiExample(
                    'Error Response',
                    value={'detail': 'Invalid or expired token'}
                ),
                OpenApiExample(
                    'Validation Error',
                    value={'non_field_errors': ['New passwords do not match.']}
                )
            ]
        )
    },
    examples=[
        OpenApiExample(
            'Reset Password Example',
            value={
                'token': 'reset_token_string',
                'new_password': 'newsecurepassword123',
                'new_password_confirm': 'newsecurepassword123'
            }
        )
    ]
)

# User profile schema
me_schema = extend_schema(
    tags=['User Profile'],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            description="User profile retrieved successfully",
            response=UserSerializer,
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={
                        'id': 1,
                        'email': 'user@example.com',
                        'full_name': 'John Doe',
                        'is_active': True,
                        'date_joined': '2023-01-01T00:00:00Z'
                    }
                )
            ]
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            description="Unauthorized",
            examples=[
                OpenApiExample(
                    'Error Response',
                    value={'detail': 'Authentication credentials were not provided.'}
                )
            ]
        )
    }
)