from django.contrib import admin
from django.urls import path

from Members.view import signup_view
from Products.view import list_items

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view.signup, name='signup'),
    path('b-sign-up/', signup_view.signup_b, name='signup_b'),
    # path('list_items/, list_items.signup_b, name='signup_b'),

]