from api.serializers.user_serializer import ForgotPasswordSerializer, CreateAccountSerializer, CredentialLoginSerializer, OtpLoginSerializer, VerifyOtpSerializer
from .models import UserOtp, User
from .authentication import create_user, login_user, check_authentication, CustomJWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from os import getenv
from dotenv import load_dotenv
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.signals import user_logged_out, user_login_failed
from datetime import timedelta
from base64 import b64decode
from rest_framework import status
import requests
import random
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import json
import secrets
from common.utils import ResponsePayload

# Create your views here.


@api_view(["POST"])
def credential_login(request: Request):
    serializer = CredentialLoginSerializer(data=request.data)
    if serializer.is_valid():
        return login_user(serializer.validated_data, request)
    else:
        return ResponsePayload().serializer_error(serializer.errors)


@api_view(["POST"])
def create_account(request: Request):
    serializer = CreateAccountSerializer(data=request.data)
    if serializer.is_valid():
        return create_user(serializer.validated_data, request)
    else:
        return ResponsePayload().serializer_error(serializer.errors)


@api_view(["POST"])
def otp_login(request: Request):
    serializer = OtpLoginSerializer(data=request.data)
    if serializer.is_valid():
        load_dotenv()
        url = "https://www.fast2sms.com/dev/bulkV2"
        otp = random.randint(100000, 999999)
        mobile_number = serializer.validated_data.get('mobile_number')
        payload = f"variables_values={otp}&route=otp&numbers={mobile_number}"
        headers = {
            'authorization': b64decode(getenv("FAST2SMS_APIKEY")).decode(),
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }

        try:
            obj = UserOtp.objects.get(mobile=mobile_number)
            obj.otp = make_password(str(otp))
            obj.attempts = obj.attempts + 1 if now() <= obj.expires_on else 1
            obj.expires_on = now() + timedelta(minutes=30)
            obj.save(update_fields=["otp", "expires_on", "attempts"])
        except UserOtp.DoesNotExist:
            obj = UserOtp.objects.create(mobile=mobile_number, otp=make_password(
                str(otp)), expires_on=now() + timedelta(minutes=30))
        except Exception as e:
            return ResponsePayload().error(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

        if obj.attempts <= 5:
            response = requests.request(
                "POST", url, data=payload, headers=headers)
            return ResponsePayload().success(data=response.json())
        else:
            user_login_failed.send(sender=User, credentials={
                                   "mobile_number": obj.mobile}, request=request)
            return ResponsePayload().error("Maximum attempts exceeded. Please try again after some time")
    else:
        return ResponsePayload().serializer_error(serializer.errors)


@api_view(["POST"])
def verify_otp(request: Request):
    serializer = VerifyOtpSerializer(data=request.data)
    if not serializer.is_valid():
        return ResponsePayload().serializer_error(serializer.errors)

    mobile_number = serializer.validated_data.get('mobile_number')
    otp = serializer.validated_data.get('otp')
    try:
        obj = UserOtp.objects.get(mobile=mobile_number)
        verified = check_password(otp, obj.otp)
        if verified and obj.attempts <= 6:
            if obj.expires_on <= now():
                return ResponsePayload().error("Oops, the OTP expired")

            obj.attempts = 0
            obj.save(update_fields=["attempts"])

            response = login_user({"email_number": obj.mobile}, request)
            if response and "error" in response.data and "code" in response.data["error"] and response.data["error"]["code"] == status.HTTP_404_NOT_FOUND:
                response = create_user(
                    {"mobile_number": obj.mobile, "password": secrets.token_urlsafe(8)}, request)
            return response

        obj.attempts = obj.attempts + 1
        obj.save(update_fields=["attempts"])
        user_login_failed.send(sender=User, credentials={
                               "mobile_number": obj.mobile}, request=request)
        return ResponsePayload().error("Incorrect OTP" if obj.attempts <= 6 else "Maximum attempts exceeded. Please try again after some time")

    except UserOtp.DoesNotExist:
        return ResponsePayload().error("Error while validating OTP")
    except Exception as e:
        return ResponsePayload().error(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def logout(request: Request):
    response = Response()
    auth_cookie = request.COOKIES.get('authToken', '')
    if not auth_cookie:
        response.data = {
            "message": "Please login to your account before logging out"}
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response
    response.delete_cookie("authToken")
    response.data = {
        "message": "User logged out successfully",
    }
    response.status_code = status.HTTP_200_OK
    try:
        user_id = RefreshToken(json.loads(auth_cookie)[
                               "refresh"]).get("user_id")
        user_logged_out.send(sender=User, user=User.objects.get(pk=user_id))
    except (TokenError, IndexError, User.DoesNotExist):
        pass
    return response


@api_view(["POST"])
def forgot_password(request: Request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(**serializer.validated_data)
            password = secrets.token_urlsafe(8)
            user.password = make_password(password)
            user.save(update_fields=["password"])
            print(password)
            """
            Email sending logic goes here
            """
            return ResponsePayload().success(data={"email": user.email})

        except User.DoesNotExist:
            return ResponsePayload().error("Sorry, we didn't find any account linked to the given details", status.HTTP_404_NOT_FOUND)
    else:
        return ResponsePayload().serializer_error(serializer.errors)


@api_view(["POST"])
def refresh_token(request: Request):
    auth_response = check_authentication(request)
    if auth_response["error_code"] == "NO_TOKEN":
        return ResponsePayload().error("Access token not found")
    elif auth_response["error_code"] == "INVALID":
        token = request.COOKIES.get("authToken")
        auth_token = json.loads(token)
        response = Response()
        try:
            generated_token = RefreshToken(auth_token["refresh"])
            auth_token["access"] = str(generated_token.access_token)
            response.status_code = status.HTTP_200_OK
            response.set_cookie("authToken", json.dumps(
                auth_token), httponly=True)
            return response
        except TokenError:
            response.delete_cookie("authToken")
            response.data = {"message": "Refresh token expired"}
            response.status_code = status.HTTP_403_FORBIDDEN
            return response
    else:
        return ResponsePayload().error("Error while parsing authentication token")
