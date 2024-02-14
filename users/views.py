from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.views import generic
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from users.models.form import PasswordChangeFormCustom, CustomUserCreationForm
from blog.models import BlogTenant

from .tokens import AccountActivationTokenGenerator

import logging
logger = logging.getLogger('django')

User = get_user_model()



def home(request):
	context = {}
	return render(request, "users/home.html", context)

def status(request):
	return HttpResponse("Funciona")


def welcome(request):
	if request.user.is_authenticated:
		return render(request, "users/welcome.html")

	return redirect(reverse("users:login"))


class RegisterView(generic.CreateView):
	template_name = "users/register.html"

	def get(self, request, *args, **kwargs):
		form = CustomUserCreationForm()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = CustomUserCreationForm(data=request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_verified = False

			# Chequear si pertenece a un tenant
			tenants = BlogTenant.objects.all()
			email_domain = user.email.split("@")[1]
			for tenant in tenants:
				if email_domain == tenant.domain:
					user.tenant = tenant.name
					break
			if not user.tenant:
				user.is_active = False
			
			form.save()
			current_site = get_current_site(request)
			
			myMail = {
					  'user':user, 
					  'domain':current_site.domain,
					  'protocol': request.scheme,
					  'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					  'token': AccountActivationTokenGenerator().make_token(user),
					  }
			if user.is_active:
				html_template = render_to_string('users/emails/register_mail.html', context= myMail)
				subject="Confirmación de registro"
				email_from = settings.EMAIL_FROM
				recipient_list = [user.email,]
				message = EmailMessage(subject, html_template, email_from, recipient_list)
				message.content_subtype = "html"
				message.send()
			return redirect(reverse("users:login"))
			
		return render(request, self.template_name, {'form': form})
	

class ActivateView(generic.CreateView):
	template_name = 'users/activate.html'

	def get(self, request, uidb64, token, *args, **kwargs):
		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user is not None and AccountActivationTokenGenerator().check_token(user, token):
			user.is_verified = True
			user.save()

			return render(request, self.template_name)
		else:
			# Eliminar usuario 
			# if token expired delete user
			try:
				user = User.objects.get(pk=uid)
				if user.is_verified == False:
					# print("Elimine el usuario")
					user.delete()
					current_site = get_current_site(request)
					context  = {'domain':current_site.domain}
					return render(request, 'users/invalid.html', context)
			except:
				pass

			return render(request, 'users/already_activate.html')


#@login_required
def register(request):
	#if request.user.id != 1:
	#	return redirect(reverse("users:login"))

	form = CustomUserCreationForm()
	if request.method == "POST":
		# Añadimos los datos recibidos al formulario
		form = CustomUserCreationForm(data=request.POST)

		if form.is_valid():
			user = form.save()

			# Si el usuario se crea correctamente 
			if user is not None:
				# Hacemos el login manualmente
				#do_login(request, user)
				return redirect('/')

	return render(request, "users/register.html", {'form': form})


@login_required
def password(request):
	context = {}

	if request.method == 'POST':
		form = PasswordChangeFormCustom(user=request.user, data=request.POST)

		if form.is_valid():
			form.save()
			# so that user does not get logged out, not working as of now.
			# TODO
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Cambio clave exitoso', extra_tags='Cambio Clave')
			return redirect('/')
		else:
			messages.error(request, 'Error', extra_tags='Cambio Clave')
			return render(request, "users/password.html", {'form': form})

	else:
		form = PasswordChangeFormCustom(user=request.user)
		context['form'] = form
		return render(request, 'users/password.html', context)


def login(request):
	form = AuthenticationForm()
	if request.method == "POST":
		# Añadimos los datos recibidos al formulario
		form = AuthenticationForm(data=request.POST)

		if form.is_valid():
			# Recuperamos las credenciales validadas
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			# Verificamos las credenciales del usuario
			user = authenticate(username=username, password=password)

			# Si existe un usuario con ese nombre y contraseña
			if user is not None:
				if not user.is_verified:
					messages.error(request, 'Usuario pendiente de verificar', extra_tags='Inicio Sesion')
					return render(request, "users/login.html", {'form': form})
				if not user.is_active:
					messages.error(request, 'Usuario inactivo', extra_tags='Inicio Sesion')
					return render(request, "users/login.html", {'form': form})

				# Hacemos el login manualmente
				do_login(request, user)
				messages.success(request, 'Inicio sesion exitoso', extra_tags='Inicio Sesion')
				# Y le redireccionamos a la portada
				return redirect('/blog/')
			else:
				messages.error(request, 'Credenciales invalidas', extra_tags='Inicio Sesion')
		else:
			messages.error(request, 'Credenciales invalidas', extra_tags='Inicio Sesion')

	return render(request, "users/login.html", {'form': form})


@login_required
def logout(request):
	do_logout(request)
	return redirect('/')
