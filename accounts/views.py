from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView

from .forms import SignUpForm
from .models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = settings.DEFAULT_DOMAIN
            context = {
                'user': user,
                'domain': current_site,
                'uid': uid,
                'token': token,
                'timeout_days': settings.PASSWORD_RESET_TIMEOUT_DAYS,
            }
            # Email for account activation
            subject = f'{user.first_name.title()}, activate your Workplan account'
            subject = ''.join(subject.splitlines())
            message = render_to_string('email/account_activation_email.html', context)
            user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
            messages.warning(request, "Please check your mailbox and complete your registration.")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


class ActivateAccount(TemplateView):
    def get(self, request, *args, **kwargs):
        user = self.get_user(kwargs.get('uidb64'))

        if self.valid(user, kwargs.get('token')):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Your account is now validate!\nand you are logged in")
            return redirect('home')

        messages.error(request, "Invalid token!")
        return redirect('home')

    def valid(self, user, token):
        token_generator = PasswordResetTokenGenerator()
        return user is not None and token_generator.check_token(user, token)

    def get_user(self, uidb64):
        try:
            user = User.objects.get(**{
                'pk': force_str(urlsafe_base64_decode(uidb64))
            })
            return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

