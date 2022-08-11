from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import Mount, Category
from django.views.generic import ListView, DetailView, CreateView, FormView
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class MountHome(DataMixin, ListView):
    model = Mount
    template_name = 'mount/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Mount.objects.filter(is_published=True).select_related('cat')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "mount/addpage.html"
    success_url = reverse_lazy('home')

    login_url = reverse_lazy('login')
    raise_exception = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить статью')
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, DetailView):
    model = Mount
    template_name = 'mount/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class MontCategory(DataMixin, ListView):
    model = Mount
    template_name = 'mount/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=str(c.pk))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Mount.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'mount/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'mount/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def about(request):
    context = {
        'title': 'О нас',
    }
    return render(request, 'mount/about.html', context=context)


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'mount/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print((form.cleaned_data))
        return redirect('home')




def contact(request):
    return HttpResponse('Форма обратной связи')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')
