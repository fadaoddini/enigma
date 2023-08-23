from django import forms

from mylogin import models


class RegisterUser(forms.ModelForm):
    class Meta:
        model = models.MyUser
        fields = ['mobile', ]