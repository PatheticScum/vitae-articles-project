from django.urls import path
from .views import *


urlpatterns = [
    path('', ArticleList.as_view(), name='index'),
    path('category/<int:pk>/', ArticleListByCategory.as_view(), name='category_list'),
    path('article/<int:pk>', ArticleDetails.as_view(), name='article_detail'),
    path('new/', NewArticle.as_view(), name='add_article'),
    path('search/', SearchResults.as_view(), name='search_results'),
    path('article/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    path('profile/', profile, name='profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', registration, name='register')
]