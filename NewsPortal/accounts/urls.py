from django.contrib.auth.views import TemplateView, LogoutView
from django.urls import path
from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('logout/confirm/', TemplateView.as_view(template_name='logout.html'), name='logout_confirm'),
]
