"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from config import settings
from mailing_management_service.views import HomeView
from users.views import ModeratorInterfaceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('moderator/', ModeratorInterfaceView.as_view(), name='moderator_interface'),

    path('blog/', include('blog.urls', namespace='blog')),
    path('user/', include('users.urls', namespace='user')),
    path('mms/', include('mailing_management_service.urls', namespace='mms')),
    path('', cache_page(60)(HomeView.as_view()), name='main'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
