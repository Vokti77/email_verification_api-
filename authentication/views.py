

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from authentication.serializers import UserSummarySerializer, UserRegistrationSerializer, ChangePasswordSerializer, PasswordResetSerializer
from django.urls import reverse
from .utils import generate_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .utils import send_activation_email

@api_view(['POST'])
def register(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_activation_email(user, request)
            return Response({"message": "User registered successfully. Check your email to verify your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user and not user.is_email_verified:
            return Response({"message": "Email is not verified. Please check your email inbox."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user:
            return Response({"message": "Invalid credentials. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        return Response({"message": f"Welcome {user.username}"})

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({"message": "Successfully logged out"})

@api_view(['GET'])
def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return Response({"message": "Email verified. You can now login."})

    return Response({"message": "Email verification failed."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)

    if serializer.is_valid():
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not user.check_password(old_password):
            return Response({"message": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully."})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def request_password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        password_reset_url = f'http://your-frontend-url/reset-password/{uid}/{token}/'
        
        # Send password reset email to the user
        # Include the password_reset_url in the email body
        
        return Response({"message": "Password reset email sent."})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Adjust permissions as needed
def user_information(request):
    users = User.objects.all()
    total_users = User.objects.count()
    user_summaries = []

    for user in users:
        login_count = user.auth_tokens.count()  # Assuming you have a related_name on the ForeignKey to User in your Token model
        last_login = user.auth_tokens.last().created if login_count > 0 else None

        user_summary = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'login_count': login_count,
            'last_login': last_login,
            'total_users': total_users,
        }
        user_summaries.append(user_summary)

    serializer = UserSummarySerializer(user_summaries, many=True)
    return Response(serializer.data)
