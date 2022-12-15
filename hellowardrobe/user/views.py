from .models import UserOtp, User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from os import getenv
from dotenv import load_dotenv
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from base64 import b64decode
from rest_framework import status
import requests
import random

# Create your views here.


@api_view(["POST"])
def send_otp(request: Request):
    load_dotenv()
    url = "https://www.fast2sms.com/dev/bulkV2"
    otp = random.randint(100000, 999999)
    mobile_number = request.data.get('mobileNumber')
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
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    response = requests.request("POST", url, data=payload, headers=headers) if obj.attempts <= 5 else {
        "details": "Maximum attempts exceeded. Please try again after some time",
        "attemptsExceeded": True}

    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_otp(request: Request):
    mobile_number = request.data.get('mobileNumber')
    otp = request.data.get("verifyOtp")
    try:
        obj = UserOtp.objects.get(mobile=mobile_number)
        verified = check_password(otp, obj.otp)
        if verified:
            if obj.expires_on <= now():
                return Response({"details": "Oops, the OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user, created = User.objects.get_or_create(
                    mobile=obj.mobile,
                    display_name=obj.mobile,
                    last_login = now()
                )
                obj.attempts = 0
                obj.save(update_fields=["attempts"])
                if not created:
                    user.last_login = now()
                    user.save(update_fields=["last_login"])
                return Response({"details": "Login successful", "id": user.id}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST)

    except UserOtp.DoesNotExist:
        return Response({"details": "Error while validating OTP"}, status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({"details": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
