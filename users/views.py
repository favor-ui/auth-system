import logging
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from django_ratelimit.decorators import ratelimit

from .serializers import (
    RegisterSerializer, LoginSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer,
    UserSerializer
)
from .utils import generate_reset_token, consume_reset_token
from auth_service.health import run_healthcheck


logger = logging.getLogger(__name__)
User = get_user_model()


@extend_schema(
    request=RegisterSerializer,
    responses={201: UserSerializer, 400: None},
    examples=[
        OpenApiExample(
            'Example',
            value={
                'email': 'user@example.com',
                'password': 'securepassword123',
                'password_confirm': 'securepassword123',
                'full_name': 'John Doe'
            }
        )
    ]
)
@api_view(["POST"])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='10/m', block=True)
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        logger.info(f"New user registered: {user.email}")
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    logger.warning(f"Registration failed: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={200: None, 400: None},
    examples=[
        OpenApiExample(
            'Example',
            value={
                'email': 'user@example.com',
                'password': 'securepassword123'
            }
        )
    ]
)
@api_view(["POST"])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='20/m', block=True)
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        
        if not user:
            logger.warning(f"Failed login attempt: {email}")
            return Response({'detail': _('Invalid credentials')}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {email}")
            return Response({'detail': _('User account is disabled.')}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        logger.info(f"User logged in: {email}")
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
    
    logger.warning(f"Login validation failed: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ForgotPasswordSerializer,
    responses={200: None, 400: None},
    examples=[
        OpenApiExample(
            'Example',
            value={
                'email': 'user@example.com'
            }
        )
    ]
)
@api_view(["POST"])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/m', block=True)
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email'].lower()
        
        # Check if user exists (without revealing existence)
        if User.objects.filter(email=email).exists():
            # Use the utility function to generate token
            token = generate_reset_token(email)
            
            # Send email with reset link
            frontend = getattr(settings, 'FRONTEND_URL', '')
            reset_link = f"{frontend}/reset?token={token}" if frontend else f"/reset?token={token}"
            
            try:
                send_mail(
                    subject=_('Password reset for your account'),
                    message=_('Use this link to reset your password: {}').format(reset_link),
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                    recipient_list=[email],
                    fail_silently=False,
                )
                logger.info(f"Password reset email sent to: {email}")
            except Exception as e:
                logger.error(f"Failed to send password reset email to {email}: {e}")
                # Still return success to avoid revealing email existence
            
            if settings.DEBUG:
                return Response({
                    'message': _('If the email exists, a reset link has been sent'),
                    'token': token  # Only return token in debug mode
                })
        
        # Always return the same message regardless of whether email exists
        return Response({'message': _('If the email exists, a reset link has been sent')})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ResetPasswordSerializer,
    responses={200: None, 400: None},
    examples=[
        OpenApiExample(
            'Example',
            value={
                'token': 'reset_token_string',
                'new_password': 'newsecurepassword123',
                'new_password_confirm': 'newsecurepassword123'
            }
        )
    ]
)
@api_view(["POST"])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/m', block=True)
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        # Use the utility function to consume the token
        email = consume_reset_token(token)
        
        if not email:
            logger.warning(f"Invalid or expired token used: {token}")
            return Response({'detail': _('Invalid or expired token')}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            logger.info(f"Password updated for user: {user.email}")
            return Response({'message': _('Password updated successfully')})
            
        except User.DoesNotExist:
            logger.error(f"User not found during password reset: {email}")
            return Response({'detail': _('User not found')}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: UserSerializer}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response(UserSerializer(user).data)

