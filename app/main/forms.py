from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class RFPAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'span2', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs={'class': 'span2', 'placeholder': 'Пароль'}))


class ParametersScan(forms.Form):
    def __init__(self, ip_targets: tuple, cve_list: tuple, *args, **kwargs):
        super(ParametersScan, self).__init__(*args, **kwargs)
        self.fields["ip_target"].choices = ip_targets
        self.fields["cve"].choices = cve_list

    ip_target = forms.ChoiceField(choices=(), required=True, label="Введите IP адрес устройства")
    cve = forms.ChoiceField(choices=(), required=True, label="Введите идентификатор уязвимости")
