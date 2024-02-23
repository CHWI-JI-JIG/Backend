from django.contrib import admin
from django.urls import path

from Members.view import member_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', member_view.signup, name='signup'),
]