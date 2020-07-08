from django.urls import path
from .views import signup
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('signup/', signup, name = 'signup'),
    path('login/', LoginView.as_view(template_name = 'user/login.html', redirect_authenticated_user = True), 
    	name = 'login'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout')
]
