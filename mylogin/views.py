from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from mylogin import forms, helper
from mylogin.models import MyUser


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


def logouti(request):
    logout(request)
    messages.info(request, "شما با موفقیت خارج شدید! ")
    return HttpResponseRedirect(reverse_lazy('index'))