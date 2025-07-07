from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'success': True,
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Handle demo login
        if username in ['admin', 'demo'] and password == 'demo':
            # Get or create demo user
            user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@demo.com',
                    'first_name': 'Demo',
                    'last_name': 'Admin',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                user.set_password('demo')
                user.save()
        else:
            user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return Response({
                'success': False,
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        # Delete the user's token
        request.user.auth_token.delete()
        return Response({
            'success': True,
            'message': 'Successfully logged out'
        })
    except:
        return Response({
            'success': True,
            'message': 'Successfully logged out'
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def forgot_password_view(request):
    """Forgot password endpoint"""
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # In a real app, you'd send an email
            # For demo purposes, we'll return the reset link
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            # Simulate sending email
            logger.info(f"Password reset link for {email}: {reset_link}")
            
            return Response({
                'success': True,
                'message': 'Password reset link sent to your email',
                'reset_link': reset_link  # Only for demo - remove in production
            })
        except User.DoesNotExist:
            # Don't reveal if email exists
            return Response({
                'success': True,
                'message': 'If an account with this email exists, a reset link has been sent'
            })
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password_view(request):
    """Reset password endpoint"""
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                
                # Invalidate all existing tokens
                Token.objects.filter(user=user).delete()
                
                return Response({
                    'success': True,
                    'message': 'Password reset successful'
                })
            else:
                return Response({
                    'success': False,
                    'error': 'Invalid or expired reset token'
                }, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'success': False,
                'error': 'Invalid reset link'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile_view(request):
    """Get current user profile"""
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined,
        'is_staff': user.is_staff,
    })
