"""solo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    path('business/add', views.create),
    path('business/addreview/<int:id>', views.addreview),
    path('business/edit/<int:id>', views.edit_business),
    path('business/<int:id>', views.show_business),
    path('category/<int:id>', views.category),
    path('logreg', views.log_reg),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
