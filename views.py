from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Article, Category
from .forms import ArticleForm, LoginForm, RegistrationForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib import messages


class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/article_lists.html'

    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('category')


class ArticleListByCategory(ArticleList):
    def get_queryset(self):
        return Article.objects.filter(
            category_id=self.kwargs['pk'], is_published=True
        ).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


class ArticleDetails(DetailView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs['pk'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        context['title'] = f"Статья {article.title}"
        return context


class NewArticle(CreateView):
    form_class = ArticleForm
    template_name = 'blog/add_article.html'
    extra_context = {
        'title': 'Добавить статью'
    }

    success_url = reverse_lazy('index')


class SearchResults(ArticleList):
    def get_queryset(self):
        word = self.request.GET.get('q')
        article = Article.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word), is_published=True
        )
        return article


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/add_article.html'


class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'


@login_required
def profile(request):
    return render(request, 'blog/profile.html', {'title': 'Ваш профиль'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались !!!')
                return redirect('index')
            else:
                messages.error(request, 'Что то не так !!!')
                return redirect('login')
        else:
            messages.error(request, 'Что то не так !!!')
            return redirect('login')
    else:
        form = LoginForm()
    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }
    return render(request, 'blog/user_login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта !!!')
    return redirect('index')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Аккаунт успешно создан !!!')
            return redirect('index')

    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }

    return render(request, 'blog/register.html', context)