from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import signup, resend_otp, login_view, profile, ChangeIntoProfile, following, followers, notifications, islogin, clear_notifications


urlpatterns = [
	path('signup/', signup, name = 'signup'),
	path('login/', login_view, name = 'login'),
	# path('login/', LoginView.as_view(template_name = 'user/login.html', redirect_authenticated_user = True), 
 #    	name = 'login'),
	path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),

	path("password-reset/", 
    	PasswordResetView.as_view(template_name='user/password_reset.html'),
    	name="password_reset"),

	path("password-reset/done/", 
		PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), 
		name="password_reset_done"),

	path("password-reset-confirm/<uidb64>/<token>/", 
		PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), 
		name="password_reset_confirm"),

	path("password-reset-complete/", 
		PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
		name="password_reset_complete"),

	path('resendOTP', resend_otp),
	path('followers', followers),
	path('following', following),
	path('notifications', notifications),
	path('notifications/clear', clear_notifications),
	path('islogin', islogin),


	path('<str:username>', profile, name='profile'),
	path('change/<str:fieldname>', ChangeIntoProfile),

	

]
