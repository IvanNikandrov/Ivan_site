from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseNotFound, Http404
from django.urls import reverse_lazy

from .forms import AddPostForm, RegisterUserForm, LoginUserForm
from .models import *
from django.views.generic import ListView, DetailView, CreateView
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class MountHome(DataMixin, ListView):
    model = Mount
    template_name = 'mount/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Mount.objects.filter(is_published=True)


# def index(request):
#     posts = Mount.objects.all()
#     context = {
#         'title': 'Главная страница',
#         'posts': posts,
#         'cat_selected': 0,
#     }
#
#     return render(request, 'mount/index.html', context=context)
#
# @login_requuired
def about(request):
    context = {
        'title': 'О нас',
    }
    return render(request, 'mount/about.html', context=context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "mount/addpage.html"
    success_url = reverse_lazy('home')

    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить статью')
        return dict(list(context.items()) + list(c_def.items()))


# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#
#     return render(request, 'mount/addpage.html', {'title': "Добавление статьи", 'form': form})


def contact(request):
    return HttpResponse('ФОрма обратной связи')


class ShowPost(DataMixin, DetailView):
    model = Mount
    template_name = 'mount/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
# post = get_object_or_404(Mount, slug=post_slug)
# context = {
#     'title': post.title,
#     'post': post,
#     'cat_selected': post.cat_id,
# }
# return render(request, 'mount/post.html', context=context)


class MontCategory(DataMixin, ListView):
    model = Mount
    template_name = 'mount/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=str(context['posts'][0].cat_id))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Mount.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


# def show_category(request, cat_id):
#     posts = Mount.objects.filter(cat_id=cat_id)
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'title': 'Отображение по рубрикам',
#         'posts': posts,
#         'cat_selected': cat_id,
#     }

# return render(request, 'mount/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')


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