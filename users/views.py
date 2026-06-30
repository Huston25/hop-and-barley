from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, UserUpdateForm
from .models import UserProfile


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()
        UserProfile.objects.create(user=user)
        login(self.request, user)
        return redirect('products:product_list')

class UserLogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')

class UserLoginView(LoginView):
   form_class = UserLoginForm
   template_name = 'login.html'
   redirect_authenticated_user = True

   def get_success_url(self):
       return reverse_lazy('products:product_list')


class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, 'account.html', context)

    def post(self, request, *args, **kwargs):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('users:account')
        else:
            messages.error(request, 'There was an error updating your account.')
            return render(request, 'account.html', {'user_form': user_form, 'profile_form': profile_form})

