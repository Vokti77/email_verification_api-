# from django.shortcuts import render, redirect
# from django.contrib import messages
# from validate_email import validate_email
# from .models import User
# from django.contrib.auth import authenticate, login, logout
# from django.urls import reverse
# from helpers.decorators import auth_user_should_not_access
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
# from .utils import generate_token
# from django.core.mail import EmailMessage
# from django.conf import settings
# import threading


# class EmailThread(threading.Thread):

#     def __init__(self, email):
#         self.email = email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()


# def send_activation_email(user, request):
#     current_site = get_current_site(request)
#     email_subject = 'Activate your account'
#     email_body = render_to_string('authentication/activate.html', {
#         'user': user,
#         'domain': current_site,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': generate_token.make_token(user)
#     })

#     email = EmailMessage(subject=email_subject, body=email_body,
#                          from_email=settings.EMAIL_FROM_USER,
#                          to=[user.email]
#                          )

#     if not settings.TESTING:
#         EmailThread(email).start()


# @auth_user_should_not_access
# def register(request):
#     if request.method == "POST":
#         context = {'has_error': False, 'data': request.POST}
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')

#         if len(password) < 6:
#             messages.add_message(request, messages.ERROR,
#                                  'Password should be at least 6 characters')
#             context['has_error'] = True

#         if password != password2:
#             messages.add_message(request, messages.ERROR,
#                                  'Password mismatch')
#             context['has_error'] = True

#         if not validate_email(email):
#             messages.add_message(request, messages.ERROR,
#                                  'Enter a valid email address')
#             context['has_error'] = True

#         if not username:
#             messages.add_message(request, messages.ERROR,
#                                  'Username is required')
#             context['has_error'] = True

#         if User.objects.filter(username=username).exists():
#             messages.add_message(request, messages.ERROR,
#                                  'Username is taken, choose another one')
#             context['has_error'] = True

#             return render(request, 'authentication/register.html', context, status=409)

#         if User.objects.filter(email=email).exists():
#             messages.add_message(request, messages.ERROR,
#                                  'Email is taken, choose another one')
#             context['has_error'] = True

#             return render(request, 'authentication/register.html', context, status=409)

#         if context['has_error']:
#             return render(request, 'authentication/register.html', context)

#         user = User.objects.create_user(username=username, email=email)
#         user.set_password(password)
#         user.save()

#         if not context['has_error']:

#             send_activation_email(user, request)

#             messages.add_message(request, messages.SUCCESS,
#                                  'We sent you an email to verify your account')
#             return redirect('login')

#     return render(request, 'authentication/register.html')


# @auth_user_should_not_access
# def login_user(request):

#     if request.method == 'POST':
#         context = {'data': request.POST}
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user and not user.is_email_verified:
#             messages.add_message(request, messages.ERROR,
#                                  'Email is not verified, please check your email inbox')
#             return render(request, 'authentication/login.html', context, status=401)

#         if not user:
#             messages.add_message(request, messages.ERROR,
#                                  'Invalid credentials, try again')
#             return render(request, 'authentication/login.html', context, status=401)

#         login(request, user)

#         messages.add_message(request, messages.SUCCESS,
#                              f'Welcome {user.username}')

#         return redirect(reverse('home'))

#     return render(request, 'authentication/login.html')


# def logout_user(request):

#     logout(request)

#     messages.add_message(request, messages.SUCCESS,
#                          'Successfully logged out')

#     return redirect(reverse('login'))


# def activate_user(request, uidb64, token):

#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))

#         user = User.objects.get(pk=uid)

#     except Exception as e:
#         user = None

#     if user and generate_token.check_token(user, token):
#         user.is_email_verified = True
#         user.save()

#         messages.add_message(request, messages.SUCCESS,
#                              'Email verified, you can now login')
#         return redirect(reverse('login'))

#     return render(request, 'authentication/activate-failed.html', {"user": user})



from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from authentication.serializers import UserSerializer, UserRegistrationSerializer, ChangePasswordSerializer, PasswordResetSerializer
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
