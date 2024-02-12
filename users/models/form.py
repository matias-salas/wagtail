from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models.custom_user import CustomUser

from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _


class PasswordChangeFormCustom(PasswordChangeForm):
    help_password = "<ul><li>Debe contener 8 caracteres como minimo<li>Debe contener 1 letra como minimo</li></ul>"
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': _("Contraseña actual incorrecta. Por favor intente nuevamente."),
        'password_length': _("Contraseña nueva debe tener 8 digitos como minimo."),
        'password_numeric': _("Contraseña nueva debe contener letras"),
    }

    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=help_password,
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    old_password = forms.CharField(
        label=_("Contraseña actual"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            if len(password1) < 8:
                raise ValidationError(
                    self.error_messages['password_length'],
                    code='password_length',
                )
            if password1.isdigit():
                raise ValidationError(
                    self.error_messages['password_numeric'],
                    code='password_numeric',
                )
        # password_validation.validate_password(password2, self.user)
        return password2


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')