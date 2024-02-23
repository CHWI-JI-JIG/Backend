from django.contrib import admin
from django.urls import path

from Members.view import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view.signup, name='signup'),
    path('b-sign-up/', signup_view.signup, name='signup'),
]