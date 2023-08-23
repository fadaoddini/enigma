import datetime
from random import randint

from ippanel import Client

from mylogin import models
from enigma.local_setting import API_MAX_SMS


def create_random_otp():
    return randint(1000, 9999)


# api sms
api_key = API_MAX_SMS
sms = Client(api_key)
credit = sms.get_credit()


def send_otp(mobile, otp):
    pattern_values = {
        "code": otp,
    }
    message_id = sms.send_pattern(
        "o81jbnw2be3lpwl",  # pattern code
        "+985000125475",  # originator
        mobile,  # recipient
        pattern_values,  # pattern values
    )
    print('OTP:', otp)


def check_otp_expiration(mobile):
    try:
        user = models.MyUser.objects.get(mobile=mobile)
        now = datetime.datetime.now()
        otp_time = user.otp_create_time
        diff_time = now - otp_time

        if diff_time.seconds > 90:
            return False
        return True
    except models.MyUser.DoesNotExist:
        return False


