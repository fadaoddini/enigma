from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from mylogin import forms, helper
from mylogin.helper import get_tokens_for_user
from mylogin.models import MyUser
import json


class RegisterView(View):
    template_name = 'web/login.html'

    def get(self, request):
        context = dict()
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)

    def post(self, request):
        context = dict()
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                user = MyUser.objects.get(mobile=mobile)
                # check otp exists
                if helper.check_otp_expiration(mobile):
                    messages.error(request, "شما به تازگی پیامکی دریافت نموده اید و هنوز معتبر می باشد!")
                    return HttpResponseRedirect(reverse_lazy('verify-otp'))
                # create otp
                otp = helper.create_random_otp()
                # send otp
                helper.send_otp(mobile, otp)
                # save otp
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                # redirect to verify
                return HttpResponseRedirect(reverse_lazy('verify-otp'))

        except MyUser.DoseNotExist:
            form = forms.RegisterUser(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # create otp
                otp = helper.create_random_otp()
                # send otp
                helper.send_otp(mobile, otp)
                # save otp
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                # redirect to verify
                return HttpResponseRedirect(reverse_lazy('verify-otp'))

        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)


class VerifyView(View):
    template_name = 'web/verify.html'
    template_name_index = 'web/index/login.html'

    def get(self, request):
        context = dict()
        return render(request, template_name=self.template_name, context=context,
                      content_type=None, status=None, using=None)

    def post(self, request):
        try:
            context = dict()
            mobile = request.session.get('user_mobile')
            user = MyUser.objects.get(mobile=mobile)
            # check otp expiration
            if not helper.check_otp_expiration(mobile):
                messages.info(request, "کد ارسال شده منقضی شده است لطفا مجدد تلاش نمائید! ")
                return HttpResponseRedirect(reverse_lazy('mylogin'))
            if user.otp != int(request.POST.get('otp')):
                messages.info(request, "کد ارسال شده مطابقت نداشت! ")
                return HttpResponseRedirect(reverse_lazy('mylogin'))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('index'))
        except MyUser.DoesNotExist:
            return render(request, template_name=self.template_name_index, context=context,
                          content_type=None, status=None, using=None)


def index(request):
    context = dict()
    return render(request, 'web/index.html', context=context)


def verify_otp(request):
    try:
        context = dict()
        mobile = request.session.get('user_mobile')
        user = MyUser.objects.get(mobile=mobile)
        if request.method == "POST":
            # check otp expiration
            if not helper.check_otp_expiration(mobile):
                messages.error(request, "کد شما اعتبار زمانی خود را از دست داده است لطفا مجددا سعی نمائید!")
                return HttpResponseRedirect(reverse_lazy('login-mobile'))
            if user.otp != int(request.POST.get('otp')):
                messages.error(request, "در وارد کردن کد ارسال شده بیشتر دقت کنید گویا اشتباه وارد می کنید!")
                return HttpResponseRedirect(reverse_lazy('login-mobile'))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('index'))
        context['mobile'] = mobile
        return render(request, 'login/verify.html', context=context)
    except MyUser.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy('login-mobile'))


def register_user(request):
    if request.user.is_authenticated:
        messages.info(request, "کاربر گرامی خوش آمدید!")
        return HttpResponseRedirect(reverse_lazy('index'))
    form = forms.RegisterUser

    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                user = MyUser.objects.get(mobile=mobile)
                # check otp exists
                if helper.check_otp_expiration(mobile):
                    messages.error(request, "شما به تازگی پیامکی دریافت نموده اید و هنوز کد شما معتبر است!")
                    return HttpResponseRedirect(reverse_lazy('verify-otp'))
                # send otp
                otp = helper.create_random_otp()
                helper.send_otp(mobile, otp)
                # save otp
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                # redirect to verify code
                return HttpResponseRedirect(reverse_lazy('verify-otp'))
        except MyUser.DoesNotExist:
            form = forms.RegisterUser(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = helper.create_random_otp()
                helper.send_otp(mobile, otp)
                # save otp
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse_lazy('verify-otp'))
    return render(request, 'web/login.html', {'form': form})


class SendOtp(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        mobile = body['mobile']

        messege = "کد تایید با موفقیت ارسال شد"
        status = "ok"
        user = MyUser.objects.filter(mobile=mobile)
        if user.exists():
            user = user.first()
            # check otp exists
            if helper.check_otp_expiration(mobile):
                messege = "شما به تازگی پیامکی دریافت نموده اید و هنوز کد شما معتبر است!"
                status = "failed"
            # send otp
            otp = helper.create_random_otp()
            helper.send_otp(mobile, otp)
            # save otp
            user.otp = otp
            user.save()
            data = {
                    'id': user.id,
                    'status': status,
                    'messege': messege,
                    'mobile': user.mobile,
                }
            return Response(data, content_type='application/json; charset=UTF-8')
        else:
            messege = "ثبت نام شدید"
            status = "ok"
            user = MyUser.objects.create(
                mobile=mobile,
            )
            # send otp
            otp = helper.create_random_otp()
            helper.send_otp(mobile, otp)
            # save otp
            user.otp = otp
            user.is_active = False
            user.save()
            data = {
                'id': user.id,
                'status': status,
                'messege': messege,
                'mobile': user.mobile,
            }
            return Response(data, content_type='application/json; charset=UTF-8')


class VerifyCode(APIView):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        mobile = body['mobile']
        code = body['code']

        messege = "کد تایید با موفقیت ارسال شد"
        status = "ok"
        user = MyUser.objects.filter(mobile=mobile)
        if user.exists():
            user = user.first()
            # res = get_tokens_for_user(mobile)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            if not helper.check_otp_expiration(mobile):
                messege = f"کد شما اعتبار زمانی خود را از دست داده است لطفا مجددا سعی نمائید!"
                status = "failed"
                refresh_token1 = "poooooch"
                access_token1 = "poooooch"
                data = {
                    'status': status,
                    'messege': messege,
                    'refresh_token': refresh_token1,
                    'access_token': access_token1,
                }
                return Response(data, content_type='application/json; charset=UTF-8')
            if user.otp != int(code):
                messege = f"در وارد کردن کد ارسال شده بیشتر دقت کنید گویا اشتباه وارد می کنید!"
                status = "failed"
                refresh_token1 = "poooooch"
                access_token1 = "poooooch"
                data = {
                    'status': status,
                    'messege': messege,
                    'refresh_token': refresh_token1,
                    'access_token': access_token1,
                }
                return Response(data)
            user.is_active = True
            user.save()
            data = {
                'status': status,
                'messege': messege,
                'refresh_token': refresh_token,
                'access_token': access_token,
            }
            return Response(data, content_type='application/json; charset=UTF-8')

        else:
            messege = f"کاربری با اطلاعات فوق وجود ندارد!"
            status = "failed"
            refresh_token = "poooooch"
            access_token = "poooooch"
            data = {
                'status': status,
                'messege': messege,
                'refresh_token': refresh_token,
                'access_token': access_token,
                'user_id': user.id,
            }
            return Response(data, content_type='application/json; charset=UTF-8')


def logouti(request):
    logout(request)
    messages.info(request, "شما با موفقیت خارج شدید! ")
    return HttpResponseRedirect(reverse_lazy('index'))