from django.urls import path
import os
from django.conf import settings
from django.conf.urls.static import static


from .views import  *


urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),

]

