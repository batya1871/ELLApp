from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm

menu_list = [
    {'ref': 'training:training_session', 'content': 'Выбор режима'},
    {'ref': 'training:statistic', 'content': 'Статистика пользователя'},
    {'ref': 'training:settings', 'content': 'Настройки'}
]


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {"title": 'Авторизация'}

    # def get_success_url(self):
    #     return reverse_lazy('training:menu')


# def login_user(request):
#     error_auth_msg = ""
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'],
#                                 password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse_lazy('training:menu'))
#             else:
#                 error_auth_msg = "Неправильный логин или пароль"
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form, 'error_auth_msg': error_auth_msg, 'is_users_app': True})
#
#
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))


#
# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return HttpResponseRedirect(reverse_lazy('users:login'))
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = "users/profile.html"
    extra_context = {
        'title': 'Изменение профиля',
        'menu_list': menu_list,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': 'Изменение пароля',
                     'menu_list': menu_list}
