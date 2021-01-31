from django.urls import path
from .views import home, follow, unfollow, post, search, add_comment, add_subcomment


urlpatterns = [
    path('', home, name = 'home'),
    path('search', search, name='search'),
    path('follow', follow),
    path('unfollow', unfollow),
    path('post', post),
    path('add_comment', add_comment),
    path('add_subcomment', add_subcomment),
]
