from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseNotFound, Http404
from django.urls import reverse_lazy

from .forms import AddPostForm
from .models import *
from django.views.generic import ListView, DetailView, CreateView


class MountHome(ListView):
    model = Mount
    template_name = 'mount/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0

        return context

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

def about(request):
    context = {
        'title': 'О нас',
    }
    return render(request, 'mount/about.html', context=context)

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = "mount/addpage.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавить статью"

        return context

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


def login(request):
    return HttpResponse('Авторизация')


class ShowPost(DetailView):
    model = Mount
    template_name = 'mount/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']

        return context
# def show_post(request, post_slug):
# post = get_object_or_404(Mount, slug=post_slug)
# context = {
#     'title': post.title,
#     'post': post,
#     'cat_selected': post.cat_id,
# }
# return render(request, 'mount/post.html', context=context)


class MontCategory(ListView):
    model = Mount
    template_name = 'mount/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id

        return context

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
